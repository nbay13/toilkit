import subprocess

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
            subprocess.run(['tar', '-xvzf', orig+'.tar.gz'])
            subprocess.run(['mv', orig, new])
            subprocess.run(['tar', '-czvf', new+'.tar.gz', new])
            subprocess.run(['rm', '-r', new])
            subprocess.run(['rm', orig+'.tar.gz'])
            subprocess.run(['mv', orig+'.sortedByCoord.md.bam', new+'.sortedByCoord.md.bam'])

