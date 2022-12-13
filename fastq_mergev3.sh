#!/usr/bin/env bash
# Need to ensure that files are in same order between paired-end reads
# 
NAMES=()
for file in ./*.gz; do
	basename=$(echo `basename "$file"` | cut -d"_" -f 1)
	echo $basename
	NAMES+=($basename)
done
U_NAMES=($(echo ${NAMES[*]} | tr ' ' '\012' | sort -u)) # unique list
mkdir -p v3_output 
LENGTH=${#U_NAMES[@]}
printf "\nMerging fastq files...\n"
for ((i=0; i < $LENGTH; i+=1)); do
	cur_base=${U_NAMES[$i]}
	echo $cur_base
	find . -type f -print | grep ${cur_base}_.*R1 | sort | xargs cat > v3_output/"${cur_base}_R1.fastq.gz"
	find . -type f -print | grep ${cur_base}_.*R2 | sort | xargs cat > v3_output/"${cur_base}_R2.fastq.gz"   
done


