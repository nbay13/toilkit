import glob
import os
import tarfile
import pandas as pd
import sys
from collections import defaultdict, OrderedDict
from tqdm import tqdm

def to_uuid_parser(args):
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

    def modify_duplicates_extract_info(tar_filename, uuid_num, results_name, infotype):
        nonlocal rsem_genes_raw_dict, rsem_genes_tpm_dict, rsem_transcripts_hugo_raw_dict, \
        rsem_transcripts_hugo_tpm_dict, rsem_transcripts_raw_dict, rsem_transcripts_tpm_dict

        gene_list = []
        gene_list_renamed = []
        raw_counts = defaultdict(list)
        tpm_counts = defaultdict(list)

        with tarfile.open(tar_filename) as tar:
            file_new_path = os.path.normpath(os.path.join(f'UUID_{uuid_num}', results_name)).replace('\\', '/')
            print("\nProcessing ", file_new_path)
            file_new = tar.extractfile(file_new_path)
            content = file_new.readlines()[1:]
            heading = [anno_dict[f"UUID_{uuid_num}"]]
            raw_counts['gene'] = heading
            tpm_counts['gene'] = heading

            for line in content:
                new_line = bytes.decode(line)
                newer_line = new_line.rstrip("\n").split("\t")
                gene_list.append(newer_line[0])
                num_copies = gene_list.count(newer_line[0])
                if num_copies == 1:
                    gene_list_renamed.append(newer_line[0])
                elif num_copies >= 2:
                    new_name = newer_line[0] + "." + str(num_copies-1)
                    gene_list_renamed.append(new_name)

                raw_counts[gene_list_renamed[-1]].append(newer_line[4])
                tpm_counts[gene_list_renamed[-1]].append(newer_line[5])

            # Update the appropriate dictionaries based on infotype
            if infotype == 'rsem_genes':
                update_global_dicts(raw_counts, tpm_counts, rsem_genes_raw_dict, rsem_genes_tpm_dict)
            elif infotype == 'rsem_transcripts_hugo':
                update_global_dicts(raw_counts, tpm_counts, rsem_transcripts_hugo_raw_dict, rsem_transcripts_hugo_tpm_dict)
            elif infotype == 'rsem_transcripts':
                update_global_dicts(raw_counts, tpm_counts, rsem_transcripts_raw_dict, rsem_transcripts_tpm_dict)
            print("Completed processing ", file_new_path, "\n")

    def update_global_dicts(raw_counts: defaultdict, tpm_counts: defaultdict, raw_dict: defaultdict(list), tpm_dict: defaultdict(list)):
        # Update global dictionaries
        for gene, raw_count in raw_counts.items():
            raw_dict[gene].extend(raw_count)

        for gene, tpm_count in tpm_counts.items():
            tpm_dict[gene].extend(tpm_count)

    def finalize_write(filename, data_dict):
        # Convert global dictionaries to DataFrames
        df = pd.DataFrame(data_dict)

        # Set index, sort columns, and transpose
        df.set_index('gene', inplace=True)
        df.sort_index(axis=1, inplace=True)
        df = df.T
        # Write to CSV
        df.to_csv(filename, sep="\t", index=True, index_label='gene')

    anno_dict = OrderedDict()

    with open(os.path.join(input_path, anno_file), 'r') as anno:
        next(anno)
        for line in anno:
            uuid, samplename = map(str.strip, line.split('\t')[:2])
            anno_dict[uuid] = samplename

    folders = glob.glob(os.path.join(input_path, 'UUID_[0-9]*.tar.gz'))
    toil_ids = [os.path.basename(directory).rsplit('.')[0] for directory in folders]

    if any(toil_id not in anno_dict for toil_id in toil_ids):
        sys.exit("Error: Missing UUID annotations")

    if any(toil_id not in toil_ids for toil_id in anno_dict):
        sys.exit("Error: Missing UUID folders")

    #for uuid_num in range(min_id, len(folders)):
    for uuid_num in tqdm(desc="Processing Samples: ", unit="samples", iterable=range(min_id, len(folders))):
        file_name = os.path.join(input_path, f"UUID_{uuid_num}.tar.gz")
        modify_duplicates_extract_info(file_name, str(uuid_num), 'RSEM/Hugo/rsem_genes.hugo.results', 'rsem_genes')
        modify_duplicates_extract_info(file_name, str(uuid_num), 'RSEM/Hugo/rsem_isoforms.hugo.results', 'rsem_transcripts_hugo')
        modify_duplicates_extract_info(file_name, str(uuid_num), 'RSEM/rsem_isoforms.results', 'rsem_transcripts')
    finalize_write(os.path.join(input_path , f"{prefix}_rsem_genes_raw_counts.txt"), rsem_genes_raw_dict)
    finalize_write(os.path.join(input_path , f"{prefix}_rsem_genes_tpm_counts.txt"), rsem_genes_tpm_dict)
    finalize_write(f"{prefix}_rsem_transcripts_hugo_raw_counts.txt", rsem_transcripts_hugo_raw_dict)
    finalize_write(f"{prefix}_rsem_transcripts_hugo_tpm_counts.txt", rsem_transcripts_hugo_tpm_dict)
    finalize_write(f"{prefix}_rsem_transcripts_raw_counts.txt", rsem_transcripts_raw_dict)
    finalize_write(f"{prefix}_rsem_transcripts_tpm_counts.txt", rsem_transcripts_tpm_dict)
