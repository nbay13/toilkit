#!/usr/bin/env bash
shopt -s nullglob
WD=$(pwd)
TDIR=$1
manifest_file="manifest-toil-rnaseq-"$2
cd "$TDIR"
arry=(*.f*q.gz)
cd $WD
starting_num=$3
echo -n "" > $manifest_file
for ((i=0, j=$starting_num; i<${#arry[@]}; j+=1,i+=2)); do echo -e "fq\tpaired\tUUID_"$j"\tfile://"$1"/"${arry[i]}",file://"$1"/"${arry[i+1]} >> "$manifest_file"; done
