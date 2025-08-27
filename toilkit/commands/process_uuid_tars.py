import glob
import os
import tarfile
import sys
import warnings
from collections import defaultdict, OrderedDict
from tqdm import tqdm
from toilkit.commands.process_uuid_tars_utilities.rsem_data import add_sample_to_header, extract_specific_counts_results, write_rsem
from toilkit.commands.process_uuid_tars_utilities.star_junctions import write_star
from toilkit.commands.process_uuid_tars_utilities.collate_qc import write_qc, prepare_read_fastqc

def process_uuid_tars(args):
    """
    Parse data from tar.gz files associated with UUIDs to return QC, RSEM, STAR junctions, etc.

    Args:
        args (argparse.Namespace): Command-line arguments.

    Returns:
        None
    """
    # Global dictionaries to accumulate data
    rsem_dict = {
        'genes_raw': defaultdict(list),
        'genes_tpm': defaultdict(list),
        'transcripts_hugo_raw': defaultdict(list),
        'transcripts_hugo_tpm': defaultdict(list),
        'transcripts_raw': defaultdict(list),
        'transcripts_tpm': defaultdict(list)
    }
    collate_qc_dict = {
        'avail_reads': [],
        'total_r1_reads': [],
        'dedup_r1_rates': [],
        'total_r2_reads': [],
        'dedup_r2_rates': [],
        'mapping_rate': [],
        'map_read_length': [],
        'multi_map_rate': [],
        'unmap_mismatch_rate': [],
        'unmap_short_rate': [],
    }
    gene_lists = {
        'genes': [],
        'transcripts_hugo': [],
        'transcripts': []
    }
    prefix = args.prefix
    anno_file = args.anno_filename
    min_id = 0
    input_path = args.indir
    star_output_path = args.star_output
    bamqc = False
    if not args.omit_bamqc:
        bamqc = True

    def open_tar_gz_for_extraction(tar_filename):
        """
        Extract specific results from a tar.gz file.

        Args:
            tar_filename (str): Path to the tar.gz file.

        Returns:
            tar folder object (tar.TarFile)
        """
        return tarfile.open(tar_filename)

    def check_missing_invalids():
        nonlocal anno_dict, min_id
        folders = glob.glob(os.path.join(input_path, 'UUID_[0-9]*.tar.gz'))
        toil_ids = [os.path.basename(directory).rsplit('.')[0] for directory in folders]
        min_id = min([int(toil_id[5:]) for toil_id in toil_ids])

        if any(toil_id not in anno_dict for toil_id in toil_ids):
            sys.exit("Error: Missing UUID annotations")

        if any(toil_id not in toil_ids for toil_id in anno_dict):
            warnings.warn("Warning: Missing UUID folders based on annotation file, proceeding with matching UUID folders")
            
        return toil_ids, folders

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
    toil_ids, folders = check_missing_invalids()
    uuid_nums = [int(toil_id[5:]) for toil_id in toil_ids]
    sorted_ids = [id for _, id in sorted(zip(uuid_nums, toil_ids))]

    for uuid in tqdm(desc="Processing Samples: ", unit="samples", iterable=sorted_ids):
        file_name = os.path.join(input_path, f"{uuid}.tar.gz")
        heading = anno_dict[f"{uuid}"]
        targz = open_tar_gz_for_extraction(file_name)
        files = targz.getnames()

        if not args.omit_rsem:
            add_sample_to_header(heading, rsem_dict['genes_raw'], rsem_dict['genes_tpm'])
            add_sample_to_header(heading, rsem_dict['transcripts_hugo_raw'], rsem_dict['transcripts_hugo_tpm'])
            add_sample_to_header(heading, rsem_dict['transcripts_raw'], rsem_dict['transcripts_tpm'])
            # Extract gene and transcript information
            print(uuid)
            extract_specific_counts_results(targz, uuid, 'RSEM/Hugo/rsem_genes.hugo.results', 'rsem_genes', rsem_dict, gene_lists, min_id)
            extract_specific_counts_results(targz, uuid, 'RSEM/Hugo/rsem_isoforms.hugo.results', 'rsem_transcripts_hugo', rsem_dict, gene_lists, min_id)
            extract_specific_counts_results(targz, uuid, 'RSEM/rsem_isoforms.results', 'rsem_transcripts', rsem_dict, gene_lists, min_id)

        if not args.omit_collate_qc:
            prepare_read_fastqc(files, targz, collate_qc_dict, bamqc)

        if not args.omit_star_junctions:
            write_star(files, targz, heading, star_output_path)
        targz.close()
        
    if not args.omit_rsem:
        print("\nWriting RSEM tsvs...")
        write_rsem(os.path.join(input_path, f"{prefix}_rsem_genes_raw_counts.txt"), rsem_dict['genes_raw'])
        write_rsem(os.path.join(input_path, f"{prefix}_rsem_genes_tpm_counts.txt"), rsem_dict['genes_tpm'])
        write_rsem(os.path.join(input_path, f"{prefix}_rsem_transcripts_hugo_raw_counts.txt"), rsem_dict['transcripts_hugo_raw'])
        write_rsem(os.path.join(input_path,f"{prefix}_rsem_transcripts_hugo_tpm_counts.txt"), rsem_dict['transcripts_hugo_tpm'])
        write_rsem(os.path.join(input_path,f"{prefix}_rsem_transcripts_raw_counts.txt"), rsem_dict['transcripts_raw'])
        write_rsem(os.path.join(input_path,f"{prefix}_rsem_transcripts_tpm_counts.txt"), rsem_dict['transcripts_tpm'])

    if not args.omit_collate_qc:
        write_qc(collate_qc_dict, bamqc, [anno_dict[id] for id in sorted_ids], sorted_ids, prefix, input_path)

    print(f"\nDone! Files can be found in {os.path.abspath(input_path)}")
