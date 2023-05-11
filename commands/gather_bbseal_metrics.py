import os
import sys
import pandas as pd
import csv
import numpy as np
import argparse

#e.g. usage: python gather_bbseal_metrics.py /media/graeberlab/My\ Book/RNA\ Batch\ 14/ Nathanson-batch-14

parser = argparse.ArgumentParser()
parser.add_argument('direc', help='The directory of the bbseal results', default = ' /media/graeberlab/My\ Book/RNA\ Batch\ 14/')
parser.add_argument('out_name', help='The prefix of the output file', default = 'Nathanson-batch-14')

args = parser.parse_args()
direc = args.direc
out_name = args.out_name

print("Directory: " + direc)
print("Output filename: " + out_name + "_BBSeal_mouse_read_filtering_results.tsv")

os.chdir(direc)

sample_direcs = [name for name in os.listdir(".") if os.path.isdir(name)]
print("BBSeal results found for these samples:\n" + '\n'.join(sample_direcs))

total_reads = []
mapped_reads = []
mouse_reads = []
human_reads = []

for d in sample_direcs:
  with open('/'.join([d, ''.join([d,"_refstats.txt"])]), 'r') as file:
    data = list(csv.reader(file, delimiter='\t'))
    total_reads.append(data[1][1])
    mapped_reads.append(data[2][1])
    human_reads.append(data[5][5])
    mouse_reads.append(data[6][5])

df = pd.DataFrame({'Sample':sample_direcs, 'Total reads':total_reads, 'Mapped reads':mapped_reads, 'Mapped Human reads': human_reads, 'Mapped Mouse reads':mouse_reads, 'Fraction Mapped Human':np.round(np.array(human_reads,dtype = 'float') / np.array(mapped_reads,dtype = 'float'),2), 'Fraction Mapped Mouse':np.round(np.array(mouse_reads,dtype = 'float') / np.array(mapped_reads,dtype = 'float'),2)})
df = df[['Sample', 'Total reads', 'Mapped reads', 'Mapped Human reads', 'Mapped Mouse reads', 'Fraction Mapped Human', 'Fraction Mapped Mouse']]
df.to_csv(out_name + "_BBSeal_mouse_read_filtering_results.tsv", sep='\t', index = False)
print("\nDone! BBSeal metrics written as .tsv to " + os.getcwd() + '\n')
