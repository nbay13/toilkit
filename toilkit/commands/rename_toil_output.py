import pysam
import os

def rename_toil_output(args):
    input_file = args.infile
    direction = args.direction

    with open(input_file, 'r') as f:
        f.readline()  # skip the first line
        for line in f:
            p = line.strip().split('\t')
            if direction == '1':
                orig = p[0]
                new = p[1]
            else:
                new = p[0]
                orig = p[1]

            # Extract and rename the BAM file
            with pysam.AlignmentFile(orig + '.sortedByCoord.md.bam', 'rb') as orig_bam:
                new_bam = pysam.AlignmentFile(new + '.sortedByCoord.md.bam', 'wb', header=orig_bam.header)
                for read in orig_bam:
                    read.query_name = new + ':' + read.query_name
                    new_bam.write(read)
                new_bam.close()

            # Cleanup original files
            os.remove(orig + '.tar.gz')
            os.remove(orig + '.sortedByCoord.md.bam')