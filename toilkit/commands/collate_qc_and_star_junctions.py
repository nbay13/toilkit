#!/usr/bin/python
'''
Author: Nick Bayley, William Huang
Last edited: 12/2023
Description: A script for collating total reads, duplication rates, and
total mapped deduplicated reads data from FastQC and BamQC results in TOIL output,
and gathering junction data from TOIL STAR output and renaming the files based on an annotation file.

'''
import sys
import os
import glob
import tarfile
import zipfile
import csv
import pandas as pd
import numpy as np
import re
import io

avail_reads = []
total_r1_reads = []
dedup_r1_rates = []
total_r2_reads = []
dedup_r2_rates = []

mapping_rate = []
map_read_length = []
multi_map_rate = []
unmap_mismatch_rate = []
unmap_short_rate = []

prefix = None
anno_filename = None
bam_qc = None
input_path = None
output_path = None
anno_dict = {}
toil_ids = []

def write_star(files, tar, i):
    global anno_dict, toil_ids, output_path
    junction_filename = list(filter(lambda x: re.search('SJ.out.tab', x), files))[0]
    file = tar.extractfile(junction_filename)
    lines = file.readlines()
    print('...Writing STAR junction file to: %s\n' % ('.'.join([anno_dict[toil_ids[i]], 'SJ.out.tab'])))
    with open('%s%s.SJ.out.tab' % (output_path, anno_dict[toil_ids[i]]), 'w') as output:
        for line in lines:
            output.write(bytes.decode(line))

'''
Unzips r1 and r2 fastqc files and extracts total reads, dedup reads , etc
'''
def prepare_read_fastqc(files, tar):
    global bam_qc, avail_reads, total_r1_reads, dedup_r1_rates, total_r2_reads, dedup_r2_rates
    for name in files:
        if 'qc.txt' in name:
            bamqc_filename = name
        elif 'R1_fastqc.zip' in name:
            r1_filename = name
        elif 'R2_fastqc.zip' in name:
            r2_filename = name
        elif 'Log.final.out' in name:
            star_filename = name
    if bam_qc:
        file = tar.extractfile(bamqc_filename)
        text_file = io.TextIOWrapper(file, encoding = 'utf-8')
        data = csv.reader(text_file, delimiter='\t')
        header = next(data)
        avail_reads.append(next(data)[1])

    r1_file = tar.extractfile(r1_filename)
    with zipfile.ZipFile(r1_file, 'r') as zip:
        with zip.open('R1_fastqc/fastqc_data.txt') as txt:
            byte_content = txt.readlines()
            content = [line.decode('utf-8') for line in byte_content]
            total_r1_reads.append(content[6].rsplit('\t')[1].strip())
            for line in content:
                if 'Total Deduplicated Percentage' in line:
                    dedup_r1_rates.append(line.rsplit('\t')[1].strip())
                    break
    r2_file = tar.extractfile(r2_filename)
    with zipfile.ZipFile(r2_file, 'r') as zip:
        with zip.open('R2_fastqc/fastqc_data.txt') as txt:
            byte_content = txt.readlines()
            content = [line.decode('utf-8') for line in byte_content]
            total_r2_reads.append(content[6].rsplit('\t')[1].strip())
            for line in content:
                if 'Total Deduplicated Percentage' in line:
                    dedup_r2_rates.append(line.rsplit('\t')[1].strip())
                    break
    star_file = tar.extractfile(star_filename)
    byte_content = star_file.readlines()
    content = [line.decode('utf-8') for line in byte_content]

    mapping_rate.append(content[9].rsplit('\t')[1].rstrip())
    map_read_length.append(content[10].rsplit('\t')[1].rstrip())
    multi_map_rate.append(content[24].rsplit('\t')[1].rstrip())
    unmap_mismatch_rate.append(content[28].rsplit('\t')[1].rstrip())
    unmap_short_rate.append(content[29].rsplit('\t')[1].rstrip())

def collate_qc_and_star_junctions(args):
    global prefix, anno_filename, bam_qc, input_path, output_path, anno_dict, toil_ids, avail_reads
    prefix = args.prefix
    anno_filename = args.anno_filename
    bam_qc = args.bamqc
    input_path = args.indir
    output_path = args.star_output

    if len(input_path) > 0:
        if input_path[-1] != "/":
            sys.exit("Error: Need forward slash at the end of input path")

    if len(output_path) > 0:
        if output_path[-1] != "/":
            sys.exit("Error: Need forward slash at the end of output path")

    if not os.path.isdir(output_path):
        print("\nCreating output folder: %s" % (output_path))
        os.mkdir(output_path)

    print("\nCollating TOIL QC and gathering STAR junction data with " + anno_filename + "\n")
    anno_dict = {}
    with open(anno_filename, "r") as anno:
        header = next(anno)
        for line in anno:
            uuid = line.split('\t')[0].strip()
            samplename = str(line.split('\t')[1]).strip()
            anno_dict[uuid] = samplename

    folders = glob.glob(input_path + 'UUID_[0-9]*.tar.gz')
    toil_ids = [os.path.basename(dir).rsplit('.')[0] for dir in folders]
    # checks if all folders are in annotation file
    if any([id not in anno_dict.keys() for id in toil_ids]):
        sys.exit("Error: Missing UUID annotations")
    # checks if all UUIDs in annotation file have a corresponding folder
    if any([id not in toil_ids for id in anno_dict.keys()]):
        sys.exit("Error: Missing UUID folders")

    for i, dir in enumerate(folders):
        print('...Accessing %s (%d/%d)' % (dir, i + 1, len(toil_ids)))
        with tarfile.open(dir) as tar:
            files = tar.getnames()
            write_star(files, tar, i)
            prepare_read_fastqc(files, tar)

    print("\nArranging final QC data table with proper sample names")
    if bam_qc:
        df = pd.DataFrame({'UUID': toil_ids, 'Total R1 reads': total_r1_reads, 'Total R2 reads': total_r2_reads,
                           'Duplication R1 rate': np.round(100 - np.array(dedup_r1_rates, dtype='float'), 2),
                           'Duplication R2 rate': np.round(100 - np.array(dedup_r2_rates, dtype='float'), 2),
                           'Mapping rate': np.round(np.array(mapping_rate, dtype='float'), 2),
                           'Avg mapped read length': np.array(map_read_length, dtype='float'),
                           'Multi-mapping rate': np.round(np.array(multi_map_rate, dtype='float'), 2),
                           'Unmapped rate (short)': np.round(np.array(unmap_short_rate, dtype='float'), 2),
                           'Unmapped rate (mismatch)': np.round(np.array(unmap_mismatch_rate, dtype='float'), 2),
                           'Total Mapped Dedup reads': avail_reads})
        df['Sample'] = [anno_dict[id] for id in toil_ids]
        df = df[['UUID', 'Sample', 'Total R1 reads', 'Total R2 reads', 'Duplication R1 rate', 'Duplication R2 rate',
                 'Mapping rate', 'Avg mapped read length', 'Multi-mapping rate', 'Unmapped rate (short)', 'Unmapped rate (mismatch)',
                 'Total Mapped Dedup reads']]
    else:
        df = pd.DataFrame({'UUID': toil_ids, 'Total R1 reads': total_r1_reads, 'Total R2 reads': total_r2_reads,
                           'Duplication R1 rate': np.round(100 - np.array(dedup_r1_rates, dtype='float'), 2),
                           'Duplication R2 rate': np.round(100 - np.array(dedup_r2_rates, dtype='float'), 2),
                           'Mapping rate': np.round(np.array(mapping_rate, dtype='float'), 2),
                           'Avg mapped read length': np.array(map_read_length, dtype='float'),
                           'Multi-mapping rate': np.round(np.array(multi_map_rate, dtype='float'), 2),
                           'Unmapped rate (short)': np.round(np.array(unmap_short_rate, dtype='float'), 2),
                           'Unmapped rate (mismatch)': np.round(np.array(unmap_mismatch_rate, dtype='float'), 2)})
        df['Sample'] = [anno_dict[id] for id in toil_ids]
        df = df[['UUID', 'Sample', 'Total R1 reads', 'Total R2 reads', 'Duplication R1 rate', 'Duplication R2 rate',
                 'Mapping rate', 'Avg mapped read length', 'Multi-mapping rate', 'Unmapped rate (short)', 'Unmapped rate (mismatch)']]
    df.to_csv(prefix + "_Toil_qc_data.tsv", sep='\t', index=False)
    print("\nDone! TOIL QC data written as .tsv to " + os.getcwd() + '\n')

    print("All Done! Renamed SJ.out.tab files can be found at: %s" % (output_path))




