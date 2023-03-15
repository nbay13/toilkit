import sys
import os
import glob
import tarfile
import zipfile
import csv
import pandas as pd
import numpy as np
import re
import argparse

'''
notes: Isoform and regular
splits into tpm and raw, so a total of 4 things collected,
only need to open twice though

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


anno_dict = {}
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

file_name = "UUID_0.tar.gz"

gene_list =[]
duplicate_genes =[]
gene_list_renamed =[]
raw_counts = {}
tpm_counts = {}
headings_list = ["gene"]

def modify_duplicates_extract_info(tar, results_name, i): #'UUID_'+str(i) + '/RSEM/Hugo/rsem_genes.hugo.results'
    file_new = tar.extractfile(results_name)
    content = file_new.readlines()[1:]
    heading = "UUID_" + str(i)
    for line in content:
        new_line = bytes.decode(line)
        newer_line = new_line.rstrip("\n").split("\t")
        gene_list.append(newer_line[0])
        value = gene_list.count(newer_line[0])
        if value == 1:
            gene_list_renamed.append(newer_line[0])
        if value >= 2:
            new_name = newer_line[0] + "." + str(value)
            gene_list_renamed.append(new_name)
    print("Modified gene_id for all duplicates.")
    headings_list.append(heading)
    for name, line in zip(gene_list_renamed, content):
        new_line = bytes.decode(line)
        newer_line = new_line.rstrip("\n").split("\t")
        raw_counts[name].append(newer_line[4])
        tpm_counts[name].append(newer_line[5])
    print("Completed " + str(i) + " file(s).")

def write_tpm_raw():
    sorted_raw = sorted(raw_counts)
    sorted_tpm = sorted(tpm_counts)
    with open(prefix + "_" + "rsem_genes_tpm_counts.txt", "w") as output:
        for item in headings_list:
            output.write(item + '\t')
        output.write("\n")
        for line in sorted_tpm:
            line_new = "\t".join(line[1])
            if line[0] == 'gene':
                continue
            output.write(line[0] + "\t" + line_new + "\n")
            
    with open(prefix + "_" + "rsem_genes_tpm_counts.txt", "r") as output:
        content = output.readlines()
    with open(prefix + "_" + "rsem_genes_tpm_counts.txt", "w") as output:
        head = content[0].rstrip("\n\t").split("\t")
        new_head = head[0]
        for word in head[1:]:
            new_head = '\t'.join([new_head, anno_dict[word]])
        output.write(new_head + '\n')
        for line in content[1:]:
            output.write(line)
    genes = pd.read_table(prefix + "_" + "rsem_genes_tpm_counts.txt", sep='\t')
    genes.sort_values(by='gene', inplace=True)
    genes.to_csv(prefix + "_" + "rsem_genes_tpm_counts.txt", sep='\t', index=False)

