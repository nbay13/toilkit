# ToilKit

A set of Python commands for working with inputs to and outputs from the [Toil RNA-Seq pipeline](https://github.com/BD2KGenomics/toil-rnaseq)

Includes additional commands for dual alignment to human and mouse genome and subsequent mouse read filtering. Pipeline configurations including reference files and directory stuctures designed for use by shared workstations in the Graeber lab @ UCLA. 

## Installation

You can install Toilkit using pip:

```bash
pip install -e git+https://github.com/nbay13/toilkit.git#egg=toilkit
```

## Usage

Toilkit provides a set of subcommands that can be used from the command line. Here's an overview of the available subcommands:

Handling fastqs:
- `fastq-merge`: Merge fastq files based on sample name
- `fastq-rename`: Rename fastqs based on key

(optional) mouse read filtering:
- `bbseal`: Run bbduk (adapter trimming) and bbseal (dual reference alignment)
- `bbcat`: Concatenate human and ambiguously-aligned reads into fastqs
- `bbmetrics`: Gather bbseal alignment metrics

Prep toil-rnaseq manifest:
- `make-manifest`: Create a toil-rnaseq manifest file
- `cut-manifest`: Split a manifest file into smaller parts
- `manifest-key`: Convert a manifest file to a sample key tsv file

Handling toil-rnaseq outputs:
- `toil-fix`: Batch rename TOIL output files with "_FAIL" suffix caused by bamQC (optional)
- `toil-combine`: Extract info from UUID_XX.tar.gz results -- such as RSEM, QC and/or STAR junctions data
- `toil-rename`: Final rename of all toil-rnaseq output files


To use a specific subcommand, run `toilkit <subcommand>`. For example:

```bash
toilkit fastq-merge --indir <input_directory> --outdir <output_directory>
```

For detailed usage instructions for each subcommand, refer to the documentation or run `toilkit <subcommand> --help`.

```
