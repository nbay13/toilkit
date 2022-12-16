# Import necessary modules
from Bio import SeqIO
import argparse
import os
import glob
import gzip

def parse():
  # Create an argument parser object
  parser = argparse.ArgumentParser()

  # Add arguments to the parser
  parser.add_argument('--indir', required=True, help='Directory containing .gz files')
  parser.add_argument('--split_char', default='_', help='Character to split file names')
  parser.add_argument('--outdir', default='.', help='Output directory')

  # Parse the command-line arguments
  return parser.parse_args()

args = parse()

# Create a list of all .gz files in the input directory
files = glob.glob(f'{args.indir}/*.gz')

# Create a list of all file base names
sample_names = []
for file in files:
    # Extract the base name of the file, using os.path.basename
    basename = os.path.basename(file).split(args.split_char)[0]
    # Append the base name to the names list
    sample_names.append(basename)

# Create a set of unique base names from the names list
unique_names = set(sample_names)

# Create the output directory, if it doesn't exist
if not os.path.exists(args.outdir):
    os.mkdir(args.outdir)

# Loop through each unique base name
for name in unique_names:
    # Print the current base name to the console
    print(name)

    # Find all files that match the pattern ${name}_.*R1 and sort them
    r1_files = sorted(glob.glob(f'{args.indir}/{name}{args.split_char}*R1*'))
    # Find all files that match the pattern ${name}_.*R2 and sort them
    r2_files = sorted(glob.glob(f'{args.indir}/{name}{args.split_char}*R2*'))

    # Create a list of tuples that pairs each R1 file with its corresponding R2 file
    file_pairs = list(zip(r1_files, r2_files))

    # Loop through each file pair
    for r1_file, r2_file in file_pairs:
        # Open the output files for writing
        with gzip.open(f'{args.outdir}/{name}_R1.fastq.gz', 'w') as output_file_r1:
            with gzip.open(f'{args.outdir}/{name}_R2.fastq.gz', 'w') as output_file_r2:
                # Iterate through the records in the input files, using SeqIO.parse
                for r1_record, r2_record in zip(SeqIO.parse(r1_file, "fastq"), SeqIO.parse(r2_file, "fastq")):
                    # Write the records to the output files, using SeqIO.write
                    SeqIO.write(r1_record, output_file_r1, "fastq")
                    SeqIO.write(r2_record, output_file_r2, "fastq")

