import os

def make_manifest(args):
    WD = args.dir
    TDIR = args.tdir
    starting_num = args.starting_num
    manifest_file = "manifest-toil-rnaseq-" + args.suffix
    os.chdir(TDIR)
    array = sorted([f for f in os.listdir(TDIR) if f.endswith(".fastq.gz") or f.endswith(".fq.gz")])
    os.chdir(WD)

    with open(manifest_file, "w") as f:
        for i, j in enumerate(range(starting_num, len(array)+starting_num, 2)):
            f.write(
                f"fq\tpaired\tUUID_{i}\tfile://{os.path.abspath(TDIR)}/{array[j]},file://{os.path.abspath(TDIR)}/{array[j + 1]}\n")
