Preparing inputs to `toil-rnaseq` with `toilkit`
================

#### Example of RNAseq fastqs fresh from UCLA TCGB core
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
### Merging fastqs
`fastq-merge` can merge fastqs from multiple lanes corresponding to the same sample 

While it is important to check for lane-specific biases in sequencing data, many tools require a single fastq file per read orientation (e.g. forward R1 and reverse R2 in paired-end sequencing).

```bash
# deafult split_char is "_", specified here for completeness
toilkit fastq-merge --indir nbayley/raw_fastqs/  --outdir nbayley/merged_fastqs/ --split_char _
24C-001
24C-002
24C-003
24C-004
```
If you are unsure how to parameterize a command, check the docstrings
```console
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
### Renaming fastqs

`fastq-rename` can rename fastqs based on a **tab-delimited** table of original and new sample names

```
24C-001	patientA
24C-002	patientB
24C-003	patientC
```
`fastq-rename` example call
```console
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
##### Notes on file renaming
- `fastq-rename` assumes that sample names in the filename are separated by "_"
- This command technically works for any file extension
- To reverse the sample renaming simply switch the order of columns in your tab-delimited key

TO ADD
================

### (optional) Mouse read filtering

### Preparing `toil-rnaseq` manifests

### Handling `toil-rnaseq` outputs

