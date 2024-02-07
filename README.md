# TOILkit

A set of Python commands for working with inputs to and outputs from the TOIL RNA-Seq pipeline. Includes additional commands for dual alignment to human and mouse genome and subsequent mouse read filtering. Pipeline configurations including reference files and directory stuctures designed for use by shared workstations in the Graeber lab @ UCLA. 

## Installation

You can install Toilkit using pip:

```bash
pip install -e git+https://github.com/nbay13/toilkit.git#egg=toilkit
```

## Usage

Toilkit provides a set of subcommands that can be used from the command line. Here's an overview of the available subcommands:

Handling fastqs:
- `fastq_merge`: Merge FASTQ files.
- `rename_by_key`: Rename files based on a key.

(optional) mouse read filtering:
- `bbduk_bbseal`: Run bbduk and bbseal.
- `cat_bbseal`: Concatenate bbseal output files.
- `gather_bbseal_metrics`: Gather bbseal metrics.

Prep toil-rnaseq manifest:
- `make_manifest`: Create a manifest file.
- `manifest_to_anno`: Convert a manifest file to an annotation file.
- `cut_manifest`: Split a manifest file into smaller parts.

Handling toil-rnaseq outputs:
- `batch_rename_TOIL_FAIL`: Batch rename TOIL output files with "_FAIL" suffix.
- `process_uuid_tars`: Extract info from UUID_X.gz tar files, such as RSEM, QC or STAR junctions data.
- `rename_toil_output`: Final rename of all TOIL output files.



To use a specific subcommand, run `toilkit <subcommand>`. For example:

```bash
toilkit fastq_merge --indir <input_directory> --outdir <output_directory>
```

For detailed usage instructions for each subcommand, refer to the documentation or run `toilkit <subcommand> --help`.

```
