import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('tdir', help = "The target directory of the fastqs")
parser.add_argument('suffix', help = "The suffix of the manifest file (ex. nathanson-15-1.tsv)")
parser.add_argument('starting_num', type = int, help = "a number for each pair of fastq files listed in the manifest file")
args = parser.parse_args()
WD = os.getcwd()
TDIR = args.tdir
starting_num = args.starting_num
manifest_file = "manifest-toil-rnaseq-" + args.suffix
os.chdir(TDIR)
array = [f for f in os.listdir(TDIR) if f.endswith(".fq.gz")]
os.chdir(WD)

with open(manifest_file, "w") as f:
    for i, j in enumerate(range(starting_num, starting_num + len(array), 2)):
        f.write(f"fq\tpaired\tUUID_{j}\tfile://{TDIR}/{array[i]},file://{TDIR}/{array[i+1]}\n")