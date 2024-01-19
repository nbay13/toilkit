import os
import tarfile
import shutil

def rename_toil_output(args):
    input_file = args.infile
    direction = args.direction
    input_dir = os.path.dirname(input_file)
    with open(input_file, 'r', encoding='utf-8') as file:
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

            # Extracting tar.gz file
            with tarfile.open(orig_tar_gz, 'r:gz') as tar:
                tar.extractall(input_dir)

            # Rename extracted folder
            os.rename(orig, new)

            # Create new tar.gz from the renamed folder
            with tarfile.open(new_tar_gz, 'w:gz') as tar:
                tar.add(new, arcname=os.path.basename(new))

            # Remove the extracted folder
            shutil.rmtree(os.path.join(input_dir, new))

            # Remove original tar.gz
            os.remove(orig_tar_gz)

            # Rename bam file
            if os.path.exists(orig_bam):
                os.rename(orig_bam, new_bam)