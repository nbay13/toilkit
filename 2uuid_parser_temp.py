import sys
import glob
from collections import defaultdict
import collections
import argparse
import pandas as pd
'''
notes:
raw genes, raw hugo transcripts, raw transcripts
tpm genes, tpm hugo transcripts, tpm transcripts

'''

prefix="LTa_xenograft"
anno_file = "annotation.tmp.txt"
min_id = 0
parser = argparse.ArgumentParser()
parser.add_argument('prefix', help='The annotation file name prefix', default = 'LTa_xenograft')
parser.add_argument('anno_filename', help='The annotation file', default = 'annotation.tmp.txt')
parser.add_argument('min_id', help = 'the minimum UUID value', default = 0)
parser.add_argument('input_dir', help='The input path of annotation data', default = '')

args = parser.parse_args()
prefix = args.prefix
anno_file = args.anno_filename
min_id = args.min_id
input_path = args.input_dir


anno_dict = collections.OrderedDict()
with open(anno_file, "r") as anno:
    header = next(anno)
    for line in anno:
        uuid = line.split('\t')[0].strip()
        samplename = str(line.split('\t')[1]).strip()
        anno_dict[uuid] = samplename

folders = glob.glob(input_path + 'UUID_[0-9]*.tar.gz')
toil_ids = [dir.rsplit('.')[0] for dir in folders]
# checks if all folders are in annotation file
if any([id not in anno_dict.keys() for id in toil_ids]):
    sys.exit("Error: Missing UUID annotations")
# checks if all UUIDs in annotation file have a corresponding folder
if any([id not in toil_ids for id in anno_dict.keys()]):
    sys.exit("Error: Missing UUID folders")


gene_list =[]
duplicate_genes =[]
gene_list_renamed =[]
raw_counts = defaultdict(list)
tpm_counts = defaultdict(list)
headings_list = ["gene"]

'''
Resets the raw and tpm count dictionaries to empty for the next gene/data type
'''
def reset():
    global raw_counts, tpm_counts
    raw_counts, tpm_counts = defaultdict(list)

'''
For a specific UUID, modifies gene id for all duplicates (ex. a 2nd occurence will have a .1 suffix to the gene name)
and extracts raw counts and transcripts per million counts for that gene, calling the write function to write to a txt.
'''
def modify_duplicates_extract_info(tar, results_name, uuid_num, type): #'UUID_'+str(i) + '/RSEM/Hugo/rsem_genes.hugo.results'
    file_new = tar.extractfile('UUID_'+str(uuid_num) + results_name)
    content = file_new.readlines()[1:]
    heading = "UUID_" + str(uuid_num)
    for line in content:
        new_line = bytes.decode(line)
        newer_line = new_line.rstrip("\n").split("\t")
        gene_list.append(newer_line[0])
        value = gene_list.count(newer_line[0])
        if value == 1:
            gene_list_renamed.append(newer_line[0])
        if value >= 2:
            new_name = newer_line[0] + "." + str(value-1)
            gene_list_renamed.append(new_name)
    print("Modified gene_id for all duplicates.")

    headings_list.append(heading)
    for name, line in zip(gene_list_renamed, content):
        new_line = bytes.decode(line).rstrip("\n").split("\t")
        raw_counts[name].append(new_line[4])
        tpm_counts[name].append(new_line[5])
    raw_outfile = prefix + "_" + "rsem_" + type + "_raw_counts.txt"
    tpm_outfile = prefix + "_" + "rsem_" + type + "_tpm_counts.txt"
    write(raw_outfile, sorted(raw_counts.items()))
    write(tpm_outfile, sorted(tpm_counts.items()))
    print("Completed " + str(uuid_num) + " file(s).")
    reset()

'''
Writes count data to a specified outfile tsv.
'''
def write(outfile, data):
    with open(outfile, "w") as output:
        for item in headings_list:
            output.write(item + '\t')
        output.write("\n")
        for line in data:
            line_new = "\t".join(line[1])
            if line[0] == 'gene':
                continue
            output.write(line[0] + "\t" + line_new + "\n")

    with open(outfile, "r") as output:
        content = output.readlines()
    with open(outfile, "w") as output:
        head = content[0].rstrip("\n\t").split("\t")
        new_head = head[0]
        for word in head[1:]:
            new_head = '\t'.join([new_head, anno_dict[word]])
        output.write(new_head + '\n')
        for line in content[1:]:
            output.write(line)
    genes = pd.read_table(outfile, sep='\t')
    genes.sort_values(by='gene', inplace=True)
    genes.to_csv(outfile, sep='\t', index=False)



for uuid_num in range(min_id, len(folders)):
    file_name = "UUID_" + str(uuid_num) + ".tar.gz"
    modify_duplicates_extract_info(file_name, uuid_num, '/RSEM/Hugo/rsem_genes.hugo.results', 'rsem_genes')
    modify_duplicates_extract_info(file_name, uuid_num, '/RSEM/Hugo/rsem_isoforms.hugo.results', 'rsem_transcripts_hugo')
    modify_duplicates_extract_info(file_name, uuid_num, '/RSEM/rsem_isoforms.results', 'rsem_transcripts')