#!/usr/bin/env bash
#get filenames
NAMES=()
for file in ./*.gz; do
	basename=$(echo `basename "$file"` | cut -d"_" -f 1)
	echo $basename
	NAMES+=($basename)
done
U_NAMES=($(echo ${NAMES[*]} | tr ' ' '\012' | sort -u)) # unique list
printf "%s\n" "${U_NAMES[@]}" > filenames.txt
# bbduk + bbseal
bbduk="/home/graeberlab/bbmap/bbduk.sh"
bbseal="/home/graeberlab/bbmap/seal.sh"
while IFS="" read -r p || [ -n "$p" ]
do
printf '%s\n' "$(date +"%D %T")"
printf '%s\n' "$p"
$bbduk in1=$p"_R1.fastq.gz" in2=$p"_R2.fastq.gz" out1=$p"_R1.trim.fq" out2=$p"_R2.trim.fq" ref=~/bbmap/resources/trim_galore_adapter.fa ktrim=r k=10 mink=7 hdist=1 tpe tbo
$bbseal in=$p"_R#.trim.fq" pattern=$p"_out_%_#.fq.gz" outu=$p"_unmapped_#.fq.gz" ambig=all ref=/media/graeberlab/wdgold/nbayley/refs/gencode.v31.transcripts.fa.gz,/media/graeberlab/wdgold/nbayley/refs/gencode.vM22.transcripts.fa.gz refstats=$p"_refstats.txt" refnames=t overwrite=t k=16
mkdir -p $p
rm $p"_R1.trim.fq"
rm $p"_R2.trim.fq"
mv $p"_out_gencode.v31.transcripts_1.fq.gz" $p
mv $p"_out_gencode.v31.transcripts_2.fq.gz" $p
mv $p"_refstats.txt" $p
mv $p"_out_gencode.vM22.transcripts_1.fq.gz" $p
mv $p"_out_gencode.vM22.transcripts_2.fq.gz" $p
mv $p"_unmapped_1.fq.gz" $p
mv $p"_unmapped_2.fq.gz" $p
done < filenames.txt
