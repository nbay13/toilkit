#!/usr/bin/env bash
# This script merges multiple .gz files in a directory into a single file.
# The files must have the same base name and be sorted in the same order.
# (Need to ensure that files are in same order between paired-end reads)

# Create an array of all file base names in the current directory
NAMES=()
for file in ./*.gz; do
  # Extract the base name of the file, using basename and cut commands
	basename=$(echo `basename "$file"` | cut -d"_" -f 1)
  # Append the base name to the NAMES array
	NAMES+=($basename)
done

# Create a new array of unique base names from the NAMES array
U_NAMES=($(echo ${NAMES[*]} | tr ' ' '\012' | sort -u))

# Create a new directory named v3_output, if it doesn't exist
mkdir -p v3_output

# Loop through each unique base name
for ((i=0; i < $LENGTH; i+=1)); do
  # Store the current base name in a variable
	cur_base=${U_NAMES[$i]}
  # Print the current base name to the console
	echo $cur_base

  # Find all files that match the pattern ${cur_base}_.*R1 and sort them
  # Concatenate the files and write the output to ${cur_base}_R1.fastq.gz in v3_output
	find . -type f -print | grep ${cur_base}_.*R1 | sort | xargs cat > v3_output/"${cur_base}_R1.fastq.gz"
  # Find all files that match the pattern ${cur_base}_.*R2 and sort them
  # Concatenate the files and write the output to ${cur_base}_R2.fastq.gz in v3_output
	find . -type f -print | grep ${cur_base}_.*R2 | sort | xargs cat > v3_output/"${cur_base}_R2.fastq.gz"
done
