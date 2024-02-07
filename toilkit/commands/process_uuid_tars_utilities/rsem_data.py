import os
import tarfile
import pandas as pd
from collections import defaultdict
from tqdm import tqdm

def extract_specific_counts_results(tar: tarfile.TarFile, uuid: str, results_name: str, infotype: str, rsem_dict: defaultdict, gene_lists, min_id: int):
        """
        Extract and process results from a specific file inside a tar.gz archive.

        Args:
            tar (tarfile.TarFile): The tarfile object.
            uuid: UUID associated with the tar.gz file.
            results_name (str): Name of the results file inside the tar.gz archive.
            infotype (str): Type of information being processed.

        Returns:
            None
        """
        gene_list = []
        gene_occurences = {}
        results_file_path = os.path.normpath(os.path.join(f'{uuid}', results_name)).replace('\\', '/')
        print("\nReading ", results_file_path)
        results_file = tar.extractfile(results_file_path)
        results_file.readline()
        
        index = 0
        for gene_entry in tqdm(results_file, desc="Processing genes", unit=' genes'):
            gene_exp_info = bytes.decode(gene_entry).rstrip("\n").split("\t")
            gene_name = gene_exp_info[0]
            uuid_num = int(uuid[5:])
            
            if uuid_num == min_id:
                if gene_name not in gene_occurences:
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
            # Update the appropriate dictionaries based on infotype
            if infotype == 'rsem_genes':
                if uuid_num == min_id:
                    gene_lists['genes'] = gene_list
                update_global_dicts(gene_lists['genes'][index], raw_count, tpm_count, rsem_dict['genes_raw'], rsem_dict['genes_tpm'])
            elif infotype == 'rsem_transcripts_hugo':
                if uuid_num == min_id:
                    gene_lists['transcripts_hugo'] = gene_list
                update_global_dicts(gene_lists['transcripts_hugo'][index], raw_count, tpm_count, rsem_dict['transcripts_hugo_raw'], rsem_dict['transcripts_hugo_tpm'])
            elif infotype == 'rsem_transcripts':
                if uuid_num == min_id:
                    gene_lists['transcripts'] = gene_list
                update_global_dicts(gene_lists['transcripts'][index], raw_count, tpm_count, rsem_dict['transcripts_raw'], rsem_dict['transcripts_tpm'])
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

def write_rsem(filename, data_dict):
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