import os
import pandas as pd
import csv
import numpy as np


def gather_bbseal_metrics(args):
  dir = args.dir
  out_name = args.outfile

  print("Directory: " + dir)
  print("Output filename: " + out_name + "_BBSeal_mouse_read_filtering_results.tsv")

  os.chdir(dir)

  sample_direcs = [name for name in os.listdir(".") if os.path.isdir(name)]
  print("BBSeal results found for these samples:\n" + '\n'.join(sample_direcs))

  total_reads = []
  mapped_reads = []
  mouse_reads = []
  human_reads = []

  for d in sample_direcs:
    with open('/'.join([d, ''.join([d, "_refstats.txt"])]), 'r') as file:
      data = list(csv.reader(file, delimiter='\t'))
      total_reads.append(data[1][1])
      mapped_reads.append(data[2][1])
      human_reads.append(data[5][5])
      mouse_reads.append(data[6][5])

  df = pd.DataFrame({'Sample': sample_direcs, 'Total reads': total_reads, 'Mapped reads': mapped_reads,
                     'Mapped Human reads': human_reads, 'Mapped Mouse reads': mouse_reads,
                     'Fraction Mapped Human': np.round(
                       np.array(human_reads, dtype='float') / np.array(mapped_reads, dtype='float'), 2),
                     'Fraction Mapped Mouse': np.round(
                       np.array(mouse_reads, dtype='float') / np.array(mapped_reads, dtype='float'), 2)})
  df = df[['Sample', 'Total reads', 'Mapped reads', 'Mapped Human reads', 'Mapped Mouse reads', 'Fraction Mapped Human',
           'Fraction Mapped Mouse']]
  df.to_csv(out_name + "_BBSeal_mouse_read_filtering_results.tsv", sep='\t', index=False)
  print("\nDone! BBSeal metrics written as .tsv to " + os.getcwd() + '\n')
