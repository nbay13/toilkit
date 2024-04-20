import os
import tarfile
import zipfile
import csv
import pandas as pd
import numpy as np
import io
from collections import defaultdict

def prepare_read_fastqc(files, tar: tarfile.TarFile, collate_qc_dict: defaultdict, bamqc: bool):
    """
    Unzips R1 and R2 fastqc files and extracts relevant QC metrics for both
    paired-end reads and STAR alignment. Updates the collate_qc_dict with
    the extracted metrics.

    Parameters:
    - files (list): List of file names within the tar archive.
    - tar (tarfile.TarFile): The opened tar archive containing the files.
    - collate_qc_dict (defaultdict): Dictionary to store collated QC metrics.
    - bamqc (bool): Flag indicating whether BAM QC data is available.

    Returns:
    None
    """
    for name in files:
        if 'qc.txt' in name:
            bamqc_filename = name
        elif 'R1_fastqc.zip' in name:
            r1_filename = name
        elif 'R2_fastqc.zip' in name:
            r2_filename = name
        elif 'Log.final.out' in name:
            star_filename = name
    if bamqc:
        file = tar.extractfile(bamqc_filename)
        text_file = io.TextIOWrapper(file, encoding = 'utf-8')
        data = csv.reader(text_file, delimiter='\t')
        header = next(data)
        collate_qc_dict['avail_reads'].append(next(data)[1])
    print('...Reading FastQC data files')

    r1_file = tar.extractfile(r1_filename)
    with zipfile.ZipFile(r1_file, 'r') as zip:
        with zip.open('R1_fastqc/fastqc_data.txt') as txt:
            byte_content = txt.readlines()
            total_line = byte_content[6].decode('utf-8')            
            dup_line = byte_content[307].decode('utf-8')
            collate_qc_dict['total_r1_reads'].append(total_line.rsplit('\t')[1].strip())           
            collate_qc_dict['dedup_r1_rates'].append(dup_line.rsplit('\t')[1].strip())

    r2_file = tar.extractfile(r2_filename)
    with zipfile.ZipFile(r2_file, 'r') as zip:
        with zip.open('R2_fastqc/fastqc_data.txt') as txt:
            byte_content = txt.readlines()
            total_line = byte_content[6].decode('utf-8')            
            dup_line = byte_content[307].decode('utf-8')
            collate_qc_dict['total_r2_reads'].append(total_line.rsplit('\t')[1].strip())           
            collate_qc_dict['dedup_r2_rates'].append(dup_line.rsplit('\t')[1].strip())

    print('...Reading STAR QC data file')    
    star_file = tar.extractfile(star_filename)
    byte_content = star_file.readlines()
    collate_qc_dict['mapping_rate'].append(byte_content[9].decode('utf-8').rsplit('\t')[1].rstrip()[:-1])
    collate_qc_dict['map_read_length'].append(byte_content[10].decode('utf-8').rsplit('\t')[1].rstrip())
    collate_qc_dict['multi_map_rate'].append(byte_content[24].decode('utf-8').rsplit('\t')[1].rstrip()[:-1])
    collate_qc_dict['unmap_mismatch_rate'].append(byte_content[28].decode('utf-8').rsplit('\t')[1].rstrip()[:-1])
    collate_qc_dict['unmap_short_rate'].append(byte_content[29].decode('utf-8').rsplit('\t')[1].rstrip()[:-1])

def create_qc_dataframe(collate_qc_dict, bamqc, sample_names, toil_ids):
    """
    Creates a pandas DataFrame from collated QC metrics.

    Parameters:
    - collate_qc_dict (defaultdict): Dictionary containing collated QC metrics.
    - bamqc (bool): Flag indicating whether BAM QC data is available.
    - sample_names (list): List of sample names.
    - toil_ids (list): List of TOIL job IDs.

    Returns:
    pandas.DataFrame: QC metrics organized in a DataFrame.
    """
    qc_columns = ['UUID', 'Sample', 'Total R1 reads', 'Total R2 reads', 'Duplication R1 rate', 'Duplication R2 rate',
                  'Mapping rate', 'Avg mapped read length', 'Multi-mapping rate', 'Unmapped rate (short)', 'Unmapped rate (mismatch)']

    qc_data = {
        'UUID': toil_ids,
        'Total R1 reads': collate_qc_dict['total_r1_reads'],
        'Total R2 reads': collate_qc_dict['total_r2_reads'],
        'Duplication R1 rate': np.round(100 - np.array(collate_qc_dict['dedup_r1_rates'], dtype='float'), 2),
        'Duplication R2 rate': np.round(100 - np.array(collate_qc_dict['dedup_r2_rates'], dtype='float'), 2),
        'Mapping rate': np.round(np.array(collate_qc_dict['mapping_rate'], dtype='float'), 2),
        'Avg mapped read length': np.array(collate_qc_dict['map_read_length'], dtype='float'),
        'Multi-mapping rate': np.round(np.array(collate_qc_dict['multi_map_rate'], dtype='float'), 2),
        'Unmapped rate (short)': np.round(np.array(collate_qc_dict['unmap_short_rate'], dtype='float'), 2),
        'Unmapped rate (mismatch)': np.round(np.array(collate_qc_dict['unmap_mismatch_rate'], dtype='float'), 2),
    }

    if bamqc:
        qc_data['Total Mapped Dedup reads'] = collate_qc_dict['avail_reads']
        qc_columns.append('Total Mapped Dedup reads')
    qc_data['Sample'] = sample_names

    df = pd.DataFrame(qc_data)
    return df[qc_columns]

def write_qc(collate_qc_dict: defaultdict, bamqc: bool, sample_names: list, toil_ids: list, prefix, output_path: str):
    """
    Writes the collated QC metrics to a TSV file.

    Parameters:
    - collate_qc_dict (defaultdict): Dictionary containing collated QC metrics.
    - bamqc (bool): Flag indicating whether BAM QC data is available.
    - sample_names (list): List of sample names.
    - toil_ids (list): List of TOIL job IDs.
    - prefix (str): Prefix for the output file.
    - output_path (str): Path for saving the output file.

    Returns:
    None
    """
    print("\nArranging final QC data table with proper sample names")
    path = os.path.join(output_path, prefix + "_toil-rnaseq_qc_data.tsv")
    df = create_qc_dataframe(collate_qc_dict, bamqc, sample_names, toil_ids)
    df.to_csv(path, sep='\t', index=False)
    print("\nDone! TOIL QC data written to " + os.path.abspath(path) + '\n')

    print("All Done! Renamed SJ.out.tab files can be found at: %s" % (os.path.abspath(output_path)))

