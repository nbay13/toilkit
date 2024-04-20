Processing inputs to and outputs from `toil-rnaseq` with `toilkit`
================

##### Example of RNAseq fastqs fresh from UCLA TCGB core
```
nbayley
│   example_sample_key.txt    
└───raw_fastqs
    │   24C-001_S4_L001_R1_001.fastq.gz
    │   24C-001_S4_L001_R2_001.fastq.gz
    │   24C-001_S4_L002_R1_001.fastq.gz
    │   24C-001_S4_L002_R2_001.fastq.gz
    │   24C-002_S5_L001_R1_001.fastq.gz
    │   24C-002_S5_L001_R2_001.fastq.gz
    │   24C-002_S5_L002_R1_001.fastq.gz
    │   24C-002_S5_L002_R2_001.fastq.gz
    │   24C-003_S6_L001_R1_001.fastq.gz
    │   24C-003_S6_L001_R2_001.fastq.gz
    │   24C-003_S6_L002_R1_001.fastq.gz
    │   24C-003_S6_L002_R2_001.fastq.gz
    └
```
## Merging fastqs
`fastq-merge` can merge fastqs from multiple lanes corresponding to the same sample 

While it is important to check for lane-specific biases in sequencing data, many tools require a single fastq file per read orientation (e.g. forward R1 and reverse R2 in paired-end sequencing).

```bash
# default split_char is "_", specified here for completeness
toilkit fastq-merge --indir nbayley/raw_fastqs/  --outdir nbayley/merged_fastqs/ --split_char _
24C-001
24C-002
24C-003
24C-004
```
If you are unsure how to parameterize a command, check the docstrings
```bash
# TODO: add defaults to docstring
toilkit fastq-merge --help

usage: toilkit fastq-merge [-h] [--indir [INDIR]] [--split_char [SPLIT_CHAR]]
                           [--outdir [OUTDIR]] [--write_method [WRITE_METHOD]]
optional arguments:
  -h, --help                    show this help message and exit
  --indir [INDIR]               Directory containing .gz files
  --split_char [SPLIT_CHAR]     Character to split file names
  --outdir [OUTDIR]             Output directory
  --write_method [WRITE_METHOD] The method of merging (p, i, or s)
```
##### Results so far
```
nbayley
│   example_sample_key.txt    
└───raw_fastqs
│   │   24C-001_S4_L001_R1_001.fastq.gz
│   │   24C-001_S4_L001_R2_001.fastq.gz
│   │   24C-001_S4_L002_R1_001.fastq.gz
│   │   24C-001_S4_L002_R2_001.fastq.gz
│   │   24C-002_S5_L001_R1_001.fastq.gz
│   │   24C-002_S5_L001_R2_001.fastq.gz
│   │   24C-002_S5_L002_R1_001.fastq.gz
│   │   24C-002_S5_L002_R2_001.fastq.gz
│   │   24C-003_S6_L001_R1_001.fastq.gz
│   │   24C-003_S6_L001_R2_001.fastq.gz
│   │   24C-003_S6_L002_R1_001.fastq.gz
│   │   24C-003_S6_L002_R2_001.fastq.gz
│   └
└───merged_fastqs
    │   24C-001_R1.fastq.gz
    │   24C-001_R2.fastq.gz
    │   24C-002_R1.fastq.gz
    │   24C-002_R2.fastq.gz
    │   24C-003_R1.fastq.gz
    │   24C-003_R2.fastq.gz
    └
```
## Renaming fastqs

`fastq-rename` can rename fastqs based on a **tab-delimited** table of original and new sample names

```
24C-001	patientA
24C-002	patientB
24C-003	patientC
```
`fastq-rename` example call
```bash
# make sure the pattern is surrounded by single or double quotes, default is '*.fastq.gz'
toilkit fastq-rename --dir nbayley/merged_fastqs/  --pattern '*.fastq.gz' --keyname nbayley/example_sample_key.txt
Directory: nbayley/merged_fastqs/
Filename pattern: *.fastq.gz
Filename key: example_sample_key.txt
{'24C-001': 'patientA', '24C-002': 'patientB', '24C-003': 'patientC'}
```
##### And the final results or merging and renaming
```
nbayley
│   example_sample_key.txt    
└───raw_fastqs
│   │   24C-001_S4_L001_R1_001.fastq.gz
│   │   24C-001_S4_L001_R2_001.fastq.gz
│   │   24C-001_S4_L002_R1_001.fastq.gz
│   │   24C-001_S4_L002_R2_001.fastq.gz
│   │   24C-002_S5_L001_R1_001.fastq.gz
│   │   24C-002_S5_L001_R2_001.fastq.gz
│   │   24C-002_S5_L002_R1_001.fastq.gz
│   │   24C-002_S5_L002_R2_001.fastq.gz
│   │   24C-003_S6_L001_R1_001.fastq.gz
│   │   24C-003_S6_L001_R2_001.fastq.gz
│   │   24C-003_S6_L002_R1_001.fastq.gz
│   │   24C-003_S6_L002_R2_001.fastq.gz
│   └
└───merged_fastqs
    │   patientA_R1.fastq.gz
    │   patientA_R2.fastq.gz
    │   patientB_R1.fastq.gz
    │   patientB_R2.fastq.gz
    │   patientC_R1.fastq.gz
    │   patientC_R2.fastq.gz
    └
```
#### Notes on file renaming
- `fastq-rename` assumes that sample names in the filename are separated by "_"
- This command technically works for any file extension
- To reverse the sample renaming simply switch the order of columns in your tab-delimited key

## Mouse read filtering

As part of our pipeline we remove mouse reads from samples taken from mice (either direct or sphere-derived xenografts). To do this we use functions from the [BBTools](https://jgi.doe.gov/data-and-tools/software-tools/bbtools/) package. Sequencing reads are aligned to both mouse and human genomes and reads that uniquely map to mouse are removed, retaining human and ambiguously mapping reads. 

##### Example of merged xenograft fastqs
```
nbayley
│   example_sample_key.txt    
└───raw_fastqs
└───merged_fastqs
    │   xenograftA_R1.fastq.gz
    │   xenograftA_R2.fastq.gz
    │   xenograftB_R1.fastq.gz
    │   xenograftB_R2.fastq.gz
    └
```

`bbseal` runs the BBduk (adapter trimming) and Seal (dual alignment) commands and produces separate fastqs for human, mouse, unaligned reads. With the hard-coded Seal paramterization in our pipeline, ambiguously aligning reads are added to both the human and mouse fastq files.

```bash
# note: currently reference file names are hard-assigned in the source code, 
# which are v31 human and vM22 mouse gtf files from GENCODE
toilkit bbseal --bbduk_dir /home/graeberlab/bbmap/ --ref_genome_dir /media/graeberlab/wdgold/nbayley/refs/
```

##### Output is a directory per sample with the BBTools Seal output (directory name based on the fastq)
```
nbayley
│   example_sample_key.txt    
└───raw_fastqs
└───merged_fastqs
    │   xenograftA_R1.fastq.gz
    │   xenograftA_R2.fastq.gz
    │   xenograftB_R1.fastq.gz
    │   xenograftB_R2.fastq.gz
    └───xenograftA
    │   │    xenograftA_unmapped_1.fq.gz
    │   │    xenograftA_out.gencode.vM22.transcripts_1.fq.gz
    │   │    xenograftA_out.gencode.vM22.transcripts_2.fq.gz
    │   │    xenograftA_out.gencode.v31.transcripts_1.fq.gz
    │   │    xenograftA_out.gencode.v31.transcripts_2.fq.gz
    │   └    xenograftA_refstats.txt
    └───xenograftB
```

`bbcat` merges the human and ambiguous reads with the unmapped reads into one fastq (per read direction)

```bash
toilkit bbcat --dir nbayley/merged_fastqs/
```
##### adds the \*_human_ambig_umap_reads_R*.fq.gz files for downstream analysis

```
nbayley
│   example_sample_key.txt    
└───raw_fastqs
└───merged_fastqs
    │   xenograftA_R1.fastq.gz
    │   xenograftA_R2.fastq.gz
    │   xenograftB_R1.fastq.gz
    │   xenograftB_R2.fastq.gz
    └───xenograftA
    │   │   xenograftA_unmapped_1.fq.gz
    │   │   xenograftA_out.gencode.vM22.transcripts_1.fq.gz
    │   │   xenograftA_out.gencode.vM22.transcripts_2.fq.gz
    │   │   xenograftA_out.gencode.v31.transcripts_1.fq.gz
    │   │   xenograftA_out.gencode.v31.transcripts_2.fq.gz
    │   │   xenograftA_human_ambig_umap_reads_R1.fq.gz
    │   │   xenograftA_human_ambig_umap_reads_R1.fq.gz
    │   └   xenograftA_refstats.txt
    └───xenograftB
```

`bbmetrics` collects the sequencing alignment metrics across multiple xenograft sequencing samples

```bash
# note: if you want spaces in the output filename prefix surround it in quotes
toilkit bbmetrics --dir nbayley/merged_fastqs/ --outfile "my example"
```

##### creates *_BBSeal_mouse_read filtering_results.tsv with alignment metrics summary

```
nbayley
│   example_sample_key.txt    
└───raw_fastqs
└───merged_fastqs
    │   xenograftA_R1.fastq.gz
    │   xenograftA_R2.fastq.gz
    │   xenograftB_R1.fastq.gz
    │   xenograftB_R2.fastq.gz
    │   my example_BBSeal_mouse_read_filtering_results.tsv
    └───xenograftA
    │   │   xenograftA_unmapped_1.fq.gz
    │   │   xenograftA_out.gencode.vM22.transcripts_1.fq.gz
    │   │   xenograftA_out.gencode.vM22.transcripts_2.fq.gz
    │   │   xenograftA_out.gencode.v31.transcripts_1.fq.gz
    │   │   xenograftA_out.gencode.v31.transcripts_2.fq.gz
    │   │   xenograftA_human_ambig_umap_reads_R1.fq.gz
    │   │   xenograftA_human_ambig_umap_reads_R1.fq.gz
    │   └   xenograftA_refstats.txt
    └───xenograftB
```

## Preparing `toil-rnaseq` manifests
Once you have prepared the fastqs, move the analysis-ready fastqs to the same directory

```
nbayley
│   example_sample_key.txt    
└───raw_fastqs
└───merged_fastqs
└───analysis_fastqs
    │   patientA_R1.fastq.gz
    │   patientA_R2.fastq.gz
    │   patientB_R1.fastq.gz
    │   patientB_R2.fastq.gz
    │   xenograftA_human_ambig_umap_reads_R1.fq.gz
    │   xenograftA_human_ambig_umap_reads_R2.fq.gz
    │   xenograftB_human_ambig_umap_reads_R1.fq.gz
    └   xenograftB_human_ambig_umap_reads_R2.fq.gz
```

`make-manifest` creates a manifest file for input to `toil-rnaseq`

```bash
# note: this command assumes paired-end sequencing fastqs (R1 and R2)
toilkit make-manifest --dir /nbayley/ --tdir /nbayley/analysis_fastqs/ --suffix my-example.tsv --starting_num 0
```

```
nbayley
│   example_sample_key.txt
│   manifest-toil-rnaseq-my-example.tsv
└───raw_fastqs
└───merged_fastqs
└───analysis_fastqs
    │   patientA_R1.fastq.gz
    │   patientA_R2.fastq.gz
    │   patientB_R1.fastq.gz
    │   patientB_R2.fastq.gz
    │   xenograftA_human_ambig_umap_reads_R1.fq.gz
    │   xenograftA_human_ambig_umap_reads_R2.fq.gz
    │   xenograftB_human_ambig_umap_reads_R1.fq.gz
    └   xenograftB_human_ambig_umap_reads_R2.fq.gz
```

`cut-manifest` splits a manifest file based on the desired number of samples per `toil-rnaseq` run

```bash
# note: files we be ordered alphanumerically and split into groups based on that order
toilkit cut-manifest --manifest_file manifest-toil-rnaseq-my-example.tsv --split_num 2
```

```
nbayley
│   example_sample_key.txt
│   manifest-toil-rnaseq-my-example.tsv
│   manifest-toil-rnaseq-my-example-1.tsv
│   manifest-toil-rnaseq-my-example-2.tsv
└───raw_fastqs
└───merged_fastqs
└───analysis_fastqs
    │   patientA_R1.fastq.gz
    │   patientA_R2.fastq.gz
    │   patientB_R1.fastq.gz
    │   patientB_R2.fastq.gz
    │   xenograftA_human_ambig_umap_reads_R1.fq.gz
    │   xenograftA_human_ambig_umap_reads_R2.fq.gz
    │   xenograftB_human_ambig_umap_reads_R1.fq.gz
    └   xenograftB_human_ambig_umap_reads_R2.fq.gz
```
Assuming you have also prepared a config.yaml you are now ready to run `toil-rnaseq run`. See the [documentation](https://github.com/BD2KGenomics/toil-rnaseq/wiki) for instructions on preparing config files and executing commands 

One more thing is to create a sample name key for converting UUIDs used by `toil-rnaseq` back to the sample names in the fastq filenames in the outputted results

```bash
# note: use the complete manifest file
toilkit manifest-key --infile nbayley/manifest-toil-rnaseq-my-example.tsv --outfile nbayley/example_UUID_key.txt
```

## Handling `toil-rnaseq` outputs

Depending on whether you enabled bamQC in the config.yaml for `toil-rnaseq`, you may have .tar.gz outputs for one or more samples containing the QC and gene expression results with the prefix "FAIL_"

```
nbayley
│   example_UUID_key.txt
│   example_sample_key.txt
│   manifest-toil-rnaseq-my-example.tsv
│   manifest-toil-rnaseq-my-example-1.tsv
│   manifest-toil-rnaseq-my-example-2.tsv
└───raw_fastqs
└───merged_fastqs
└───analysis_fastqs
└───toil_output
    │   UUID_0.tar.gz
    │   UUID_1.tar.gz
    │   FAIL.UUID_2.tar.gz
    │   UUID_3.tar.gz
    │   UUID_0.sortedByCoord.md.bam
    │   UUID_1.sortedByCoord.md.bam
    │   UUID_2.sortedByCoord.md.bam
    └   UUID_3.sortedByCoord.md.bam
```

`toil-fix` removes the FAIL prefix from outputs (don't worry we will pull out the relevant QC data related to the FAIL prefix later!)

```bash
toilkit toil-fix --indir nbayley/toil_output/
```

##### original .tar.gz files are moved into a *renamed* directory within the working directory
```
nbayley
│   example_UUID_key.txt
│   example_sample_key.txt
│   manifest-toil-rnaseq-my-example.tsv
│   manifest-toil-rnaseq-my-example-1.tsv
│   manifest-toil-rnaseq-my-example-2.tsv
└───raw_fastqs
└───merged_fastqs
└───analysis_fastqs
└───toil_output
    │   UUID_0.tar.gz
    │   UUID_1.tar.gz
    │   UUID_2.tar.gz
    │   UUID_3.tar.gz
    │   UUID_0.sortedByCoord.md.bam
    │   UUID_1.sortedByCoord.md.bam
    │   UUID_2.sortedByCoord.md.bam
    │   UUID_3.sortedByCoord.md.bam
    └───renamed
        │   FAIL.UUID_3.tar.gz
        └
```

`toil-combine` is the primary command for extracting all relevant information from the .tar.gz and compiling the data across samples. By default this command will extract and collate FastQC and STAR alignment results, bamQC results, RSEM gene/isoform expression results, and STAR junction alignment results. Check the docstrings to see how to omit specific results.


```bash
# note: currently this command will output results in the current working directory. Let's assume we are in the directory *../nbayley/*
toilkit toil-combine --prefix my_example --anno_filename example_UUID_key.txt --indir toil_output/ --star_output junctions/
```

##### The default command will produce results like this
```
nbayley
│   example_UUID_key.txt
│   example_sample_key.txt
│   manifest-toil-rnaseq-my-example.tsv
│   manifest-toil-rnaseq-my-example-1.tsv
│   manifest-toil-rnaseq-my-example-2.tsv
│   my_example_rsem_genes_raw_counts.txt
│   my_example_rsem_genes_tpm_counts.txt
│   my_example_rsem_transcripts_hugo_raw_counts.txt
│   my_example_rsem_transcripts_hugo_tpm_counts.txt
│   my_example_rsem_transcripts_raw_counts.txt
│   my_example_rsem_transcripts_raw_counts.txt
│   my_example_toil-rnaseq_qc_data.txt
└───raw_fastqs
└───merged_fastqs
└───analysis_fastqs
└───toil_output
```

The last thing to do is rename the `toil-rnaseq` output files with UUIDs back to our sample names using `toil-rename`. Currently this command **must** come after `toil-combine` because it expects UUID outputs

```bash
# note: currently this command operates in the current working directory. Let's assume we `cd` into *../nbayley/toil_output/*
toilkit toil-rename --infile ../example_UUID_key.txt
```

If you accidentally rename the output files before `toil-combine` you can easily reverse the renaming
```bash
toilkit toil-rename --infile ../example_UUID_key.txt --direction 2
```

Assuming all went well you now have all the QC, gene expression, and splice junction data extracted from the .tar.gz outputs and output filenames that correspond to biological samples :D

##### Final renamed outputs
```
nbayley
│   example_UUID_key.txt
│   example_sample_key.txt
│   manifest-toil-rnaseq-my-example.tsv
│   manifest-toil-rnaseq-my-example-1.tsv
│   manifest-toil-rnaseq-my-example-2.tsv
│   my_example_rsem_genes_raw_counts.txt
│   my_example_rsem_genes_tpm_counts.txt
│   my_example_rsem_transcripts_hugo_raw_counts.txt
│   my_example_rsem_transcripts_hugo_tpm_counts.txt
│   my_example_rsem_transcripts_raw_counts.txt
│   my_example_rsem_transcripts_raw_counts.txt
│   my_example_toil-rnaseq_qc_data.txt
└───raw_fastqs
└───merged_fastqs
└───analysis_fastqs
└───toil_output
    │   patientA.tar.gz
    │   patientB.tar.gz
    │   xenograftA.tar.gz
    │   xenograftB.tar.gz
    │   patientA.sortedByCoord.md.bam
    │   patientB.sortedByCoord.md.bam
    │   xenograftA.sortedByCoord.md.bam
    │   xenograftB.sortedByCoord.md.bam
    └───renamed
        │   FAIL.UUID_3.tar.gz
        └
```

#### Final notes
- By default many of the commands will assume the current working directory is the input directory if not provided by a parameter (e.g. \-\-dir or \-\-indir)
- Many parameters specified here for completeness have reasonable defaults so you don't have to parameterize every command, check the docstrings!


# TODO 
- example of mouse read stats summary
- example of manifest
- example `toil-rnaseq` command
- example of QC outputs
- write full documentation