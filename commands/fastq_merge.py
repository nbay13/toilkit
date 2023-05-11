# Import necessary modules
from Bio import SeqIO
import argparse
import os
import glob
import gzip
import subprocess

    # Parses user input in the form of python fastq_merge.py --indir --split_char --outdir -- write_method
# Uses SeqIO Parse to write R1 and R2 inputs to merged file
def seqIO_parse_merge(names,args):
    for name in names:
        print(name)
        # Find all files that match the pattern ${name}_.*R1 and sort them
        r1_files = sorted(glob.glob(f'{args.indir}/{name}{args.split_char}*R1*'))
        # Find all files that match the pattern ${name}_.*R2 and sort them
        r2_files = sorted(glob.glob(f'{args.indir}/{name}{args.split_char}*R2*'))
        # Create a list of tuples that pairs each R1 file with its corresponding R2 file
        file_pairs = list(zip(r1_files, r2_files))
        # Loop through each file pair
        for r1_file, r2_file in file_pairs:
            print(r1_file, r2_file)
            # Open the output files for writing
            with gzip.open(f'{args.outdir}/{name}_R1.fastq.gz', 'at') as output_file_r1:
                with gzip.open(f'{args.outdir}/{name}_R2.fastq.gz', 'at') as output_file_r2:
                    # Iterate through the records in the input files, using SeqIO.parse
                    for r1_record, r2_record in zip(SeqIO.parse(gzip.open(r1_file, "rt"), "fastq"),
                                                    SeqIO.parse(gzip.open(r2_file, "rt"), "fastq")):
                        # Write the records to the output files, using SeqIO.write
                        SeqIO.write(r1_record, output_file_r1, "fastq")
                        SeqIO.write(r2_record, output_file_r2, "fastq")


# Uses SeqIO Index to write R1 and R2 inputs to merged file
def seqIO_index_merge(names, args):
    for name in names:
        print(name)
        # Find all files that match the pattern ${name}_.*R1 and sort them
        r1_files = sorted(glob.glob(f'{args.indir}/{name}{args.split_char}*R1*'))
        # Find all files that match the pattern ${name}_.*R2 and sort them
        r2_files = sorted(glob.glob(f'{args.indir}/{name}{args.split_char}*R2*'))
        # Create a list of tuples that pairs each R1 file with its corresponding R2 file
        file_pairs = list(zip(r1_files, r2_files))
        # Loop through each file pair
        for r1_file, r2_file in file_pairs:
            # Index the input files
            index_r1 = SeqIO.index(r1_file, "fastq")
            index_r2 = SeqIO.index(r2_file, "fastq")
            # Open the output files for writing
            with gzip.open(f'{args.outdir}/{name}_R1.fastq.gz', 'w') as output_file_r1:
                with gzip.open(f'{args.outdir}/{name}_R2.fastq.gz', 'w') as output_file_r2:
                    # Iterate through the records in the input files, using SeqIO.parse
                    for record_id in index_r1:
                        # Retrieve the record from the indexed file
                        record_r1 = SeqIO.read(gzip.open(index_r1, "rt"), "fastq", record_id)
                        record_r2 = SeqIO.read(gzip.open(index_r2, "rt"), "fastq", record_id)

                        # Write the record to the output file
                        SeqIO.write(record_r1, output_file_r1, "fastq")
                        SeqIO.write(record_r2, output_file_r2, "fastq")
        # It is important to note that this version of the code assumes
        # that the records in the R1 and R2 files have the same record IDs,
        # and that the records are in the same order in both files.


# Uses Subprocess with cat command to write R1 and R2 inputs to merged file
def subprocess_merge(names, args):
    for cur_base in names:
        print(cur_base)
        # Find and concatenate the files and write the output to ${cur_base}_R1.fastq.gz in outdir

        command_r1 = f'find {args.indir} -type f -name "{cur_base}{args.split_char}*R1*" | sort | xargs cat > ' \
                     f'{args.outdir}/{cur_base}_R1.fastq.gz'
        subprocess.run(command_r1, shell=True)

        command_r2 = f'find {args.indir} -type f -name "{cur_base}{args.split_char}*R2*" | sort | xargs cat >' \
                     f' {args.outdir}/{cur_base}_R2.fastq.gz'
        subprocess.run(command_r2, shell=True)


# Parses user input in the form of python fastq_merge.py indir split_char outdir write_method
def parse_merge_args(args):
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
    unique_names = sorted(set(sample_names))
    # Create the output directory, if it doesn't exist
    if not os.path.exists(args.outdir):
        os.mkdir(args.outdir)
    # does the specified write method
    if args.write_method == 's':
        subprocess_merge(unique_names, args)
    elif args.write_method == 'p':
        seqIO_parse_merge(unique_names, args)
    elif args.write_method == 'i':
        seqIO_index_merge(unique_names, args)
