import os

def make_manifest(args):
    WD = args.dir  # Directory where the manifest file will be created
    TDIR = args.tdir  # Directory where the .fastq.gz or .fq.gz files are located
    starting_num = args.starting_num
    manifest_file = os.path.join(WD, "manifest-toil-rnaseq-" + args.suffix)

    # List all relevant files in the Target Directory
    file_list = sorted([f for f in os.listdir(TDIR) if f.endswith(".fastq.gz") or f.endswith(".fq.gz")])

    with open(manifest_file, "w") as f:
        for i in range(0, len(file_list), 2):
            fq1 = "file://" + os.path.abspath(os.path.join(TDIR, file_list[i]))
            fq2 = "file://" + os.path.abspath(os.path.join(TDIR, file_list[i + 1]))
            f.write(f"fq\tpaired\tUUID_{starting_num + int(i / 2)}\t{fq1},{fq2}\n")
