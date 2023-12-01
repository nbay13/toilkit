import glob
import os
import tarfile
import pandas as pd
import sys
from collections import defaultdict, OrderedDict
from tqdm import tqdm

def to_uuid_parser(args):
    """
    Parse RSEM results from tar.gz files associated with UUIDs and return TSVs.

    Args:
        args (argparse.Namespace): Command-line arguments.

    Returns:
        None
    """
    # Global dictionaries to accumulate data
    rsem_genes_raw_dict = defaultdict(list)
    rsem_genes_tpm_dict = defaultdict(list)
    rsem_transcripts_hugo_raw_dict = defaultdict(list)
    rsem_transcripts_hugo_tpm_dict = defaultdict(list)
    rsem_transcripts_raw_dict = defaultdict(list)
    rsem_transcripts_tpm_dict = defaultdict(list)

    prefix = args.prefix
    anno_file = args.anno_filename
    min_id = int(args.min_id)
    input_path = args.input_dir

    gene_list = []
    gene_set = set()
    gene_occurences = {}

    def open_tar_gz_for_extraction(tar_filename):
        """
        Extract specific results from a tar.gz file.

        Args:
            tar_filename (str): Path to the tar.gz file.

        Returns:
            None
        """
        with tarfile.open(tar_filename) as tar:
            # Extract gene and transcript information
            extract_specific_results(tar, str(uuid_num), 'RSEM/Hugo/rsem_genes.hugo.results', 'rsem_genes')
            extract_specific_results(tar, str(uuid_num), 'RSEM/Hugo/rsem_isoforms.hugo.results', 'rsem_transcripts_hugo')
            extract_specific_results(tar, str(uuid_num), 'RSEM/rsem_isoforms.results', 'rsem_transcripts')

    def extract_specific_results(tar: tarfile.TarFile, uuid_num: str, results_name, infotype):
        """
        Extract and process results from a specific file inside a tar.gz archive.

        Args:
            tar (tarfile.TarFile): The tarfile object.
            uuid_num (str): UUID associated with the tar.gz file.
            results_name (str): Name of the results file inside the tar.gz archive.
            infotype (str): Type of information being processed.

        Returns:
            None
        """
        nonlocal rsem_genes_raw_dict, rsem_genes_tpm_dict, rsem_transcripts_hugo_raw_dict, \
        rsem_transcripts_hugo_tpm_dict, rsem_transcripts_raw_dict, rsem_transcripts_tpm_dict, gene_list, gene_set
        results_file_path = os.path.normpath(os.path.join(f'UUID_{uuid_num}', results_name)).replace('\\', '/')
        print("\nProcessing ", results_file_path)
        results_file = tar.extractfile(results_file_path)
        results_file.readline()
        
        index = 0
        for gene_entry in tqdm(results_file, desc="Processing genes", unit=' genes'):
            gene_exp_info = bytes.decode(gene_entry).rstrip("\n").split("\t")
            gene_name = gene_exp_info[0]
            
            if int(uuid_num) == min_id:
                if gene_name not in gene_set:
                    gene_set.add(gene_name)
                    gene_occurences[gene_name] = 1
                    gene_list.append(gene_name)
                else:
                    # If the gene is already in the set, append a modified name
                    gene_occurences[gene_name] += 1
                    num_copies = gene_occurences[gene_name]
                    gene_name = f"{gene_name}.{num_copies-1}"
                    gene_list.append(gene_name)

            raw_count = gene_exp_info[4]
            tpm_count = gene_exp_info[5]
            print(gene_name, gene_list[index])
            # Update the appropriate dictionaries based on infotype
            if infotype == 'rsem_genes':
                update_global_dicts(gene_list[index], raw_count, tpm_count, rsem_genes_raw_dict, rsem_genes_tpm_dict)
            elif infotype == 'rsem_transcripts_hugo':
                update_global_dicts(gene_list[index], raw_count, tpm_count, rsem_transcripts_hugo_raw_dict, rsem_transcripts_hugo_tpm_dict)
            elif infotype == 'rsem_transcripts':
                update_global_dicts(gene_list[index], raw_count, tpm_count, rsem_transcripts_raw_dict, rsem_transcripts_tpm_dict)
            index += 1

        print("Completed processing ", results_file_path, "\n")

    def add_sample_to_header(sample: str, raw_dict: defaultdict(list), tpm_dict: defaultdict(list)):
        """
        Add sample information to the header of data dictionaries.

        Args:
            sample (str): Sample information.
            raw_dict (defaultdict): Dictionary for raw counts.
            tpm_dict (defaultdict): Dictionary for TPM counts.

        Returns:
            None
        """
        raw_dict['gene'].append(sample)
        tpm_dict['gene'].append(sample)

    def update_global_dicts(gene_name: str, raw_count: float, tpm_count: float, raw_dict: defaultdict(list), tpm_dict: defaultdict(list)):
        """
        Update global dictionaries with gene information.

        Args:
            gene_name (str): Gene name.
            raw_count (float): Raw count value.
            tpm_count (float): TPM count value.
            raw_dict (defaultdict): Dictionary for raw counts.
            tpm_dict (defaultdict): Dictionary for TPM counts.

        Returns:
            None
        """
        raw_dict[gene_name].append(raw_count)
        tpm_dict[gene_name].append(tpm_count)

    def finalize_write(filename, data_dict):
        """
        Convert global dictionaries to DataFrames and write to CSV.

        Args:
            filename (str): Name of the output CSV file.
            data_dict (defaultdict): Dictionary containing gene expression data.

        Returns:
            None
        """
        df = pd.DataFrame(data_dict)
        
        # Set index, sort columns, and transpose
        df.set_index('gene', inplace=True)
        df.sort_index(axis=1, inplace=True)
        df = df.T
        # Write to CSV
        df.to_csv(filename, sep="\t", index=True, index_label='gene')

    def check_missing_invalids():
        nonlocal anno_dict
        folders = glob.glob(os.path.join(input_path, 'UUID_[0-9]*.tar.gz'))
        toil_ids = [os.path.basename(directory).rsplit('.')[0] for directory in folders]

        if any(toil_id not in anno_dict for toil_id in toil_ids):
            sys.exit("Error: Missing UUID annotations")

        if any(toil_id not in toil_ids for toil_id in anno_dict):
            sys.exit("Error: Missing UUID folders")
            
        return folders

    def map_uuid_to_sample_id():
        dict = OrderedDict()

        with open(os.path.join(input_path, anno_file), 'r') as anno:
            next(anno)
            for line in anno:
                uuid, samplename = map(str.strip, line.split('\t')[:2])
                dict[uuid] = samplename

        return dict
    
#############################################################################################################

    anno_dict = map_uuid_to_sample_id()
    folders = check_missing_invalids()

    for uuid_num in tqdm(desc="Processing Samples: ", unit="samples", iterable=range(min_id, len(folders))):
        file_name = os.path.join(input_path, f"UUID_{uuid_num}.tar.gz")
        heading = anno_dict[f"UUID_{uuid_num}"]
        add_sample_to_header(heading, rsem_genes_raw_dict, rsem_genes_tpm_dict)
        add_sample_to_header(heading, rsem_transcripts_hugo_raw_dict, rsem_transcripts_hugo_tpm_dict)
        add_sample_to_header(heading, rsem_transcripts_raw_dict, rsem_transcripts_tpm_dict)
        open_tar_gz_for_extraction(file_name)
        
    finalize_write(os.path.join(input_path, f"{prefix}_rsem_genes_raw_counts.txt"), rsem_genes_raw_dict)
    finalize_write(os.path.join(input_path, f"{prefix}_rsem_genes_tpm_counts.txt"), rsem_genes_tpm_dict)
    # finalize_write(f"{prefix}_rsem_transcripts_hugo_raw_counts.txt", rsem_transcripts_hugo_raw_dict)
    # finalize_write(f"{prefix}_rsem_transcripts_hugo_tpm_counts.txt", rsem_transcripts_hugo_tpm_dict)
    # finalize_write(f"{prefix}_rsem_transcripts_raw_counts.txt", rsem_transcripts_raw_dict)
    # finalize_write(f"{prefix}_rsem_transcripts_tpm_counts.txt", rsem_transcripts_tpm_dict)
