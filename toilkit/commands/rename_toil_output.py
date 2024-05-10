import os
import tarfile
import shutil
import datetime

def rename_toil_output(args):
    input_file = args.infile
    direction = args.direction
    input_dir = args.indir
    with open(input_file, 'r', encoding='utf-8') as file:
        header = next(file)
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue

            if direction == 1:
                orig, new = parts[0], parts[1]
            else:
                new, orig = parts[0], parts[1]

            orig_tar_gz = os.path.join(input_dir, orig + ".tar.gz")
            new_tar_gz = os.path.join(input_dir, new + ".tar.gz")
            orig_bam = os.path.join(input_dir, orig + ".sortedByCoord.md.bam")
            new_bam = os.path.join(input_dir, new + ".sortedByCoord.md.bam")
            print("Renaming ", new, "toil-rnaseq outputs...")
            if os.path.exists(orig_tar_gz):
                rename_tar(orig_tar_gz, new_tar_gz, input_dir, orig, new)
            if os.path.exists(orig_bam):
                rename_bam(orig_bam, new_bam)
    tprint("Done!")



def rename_tar(orig_tar_gz: str, new_tar_gz: str, input_dir: str, orig, new):
    # Extracting tar.gz file
    with tarfile.open(orig_tar_gz, 'r:gz') as tar:
        tar.extractall(input_dir)

    # Rename extracted folder
    os.rename(os.path.join(input_dir, orig), os.path.join(input_dir, new))

    # Create new tar.gz from the renamed folder
    with tarfile.open(new_tar_gz, 'w:gz') as tar:
        tar.add(os.path.join(input_dir,new), arcname=os.path.basename(new))

    # Remove the extracted folder
    shutil.rmtree(os.path.join(input_dir, new))

    # Remove original tar.gz
    os.remove(orig_tar_gz)
    
def rename_bam(orig_bam: str, new_bam: str):
    # Rename bam file
    os.rename(orig_bam, new_bam)

def tprint(s):
    # Python 3
    time_format = "%a %b %d %H:%M:%S"
    print('[{}] {}'.format(datetime.datetime.now().strftime(time_format), s))