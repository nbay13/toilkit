#!/usr/bin/env bash
for f in */; do
f=${f%*/}
cd $f
echo $f
cat ${f}_out_gencode.v31.transcripts_1.fq.gz ${f}_unmapped_1.fq.gz > ${f}_human_ambig_umap_reads_R1.fq.gz;
cat ${f}_out_gencode.v31.transcripts_2.fq.gz ${f}_unmapped_2.fq.gz > ${f}_human_ambig_umap_reads_R2.fq.gz;
cd ..
done
