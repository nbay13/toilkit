import subprocess
import os
import datetime
import glob

def bbduk_bbseal(args):
    bbduk = args.bbdukdir + '/bbduk.sh'
    bbseal = args.bbdukdir + '/bbseal.sh'

    # get filenames
    NAMES = []
    for file in glob.glob('*.gz'):
        basename = os.path.basename(file).split('_')[0]
        print(basename)
        NAMES.append(basename)
    U_NAMES = list(set(NAMES))  # unique list
    with open('filenames.txt', 'w') as f:
        for name in U_NAMES:
            f.write(name + '\n')

    with open('filenames.txt', 'r') as f:
        for p in f.readlines():
            p = p.strip()
            print(f'{p} started at {datetime.datetime.now()}')
            subprocess.run(
                [bbduk, f'in1={p}_R1.fastq.gz', f'in2={p}_R2.fastq.gz', f'out1={p}_R1.trim.fq', f'out2={p}_R2.trim.fq',
                 'ref=~/bbmap/resources/trim_galore_adapter.fa', 'ktrim=r', 'k=10', 'mink=7', 'hdist=1', 'tpe', 'tbo'])
            subprocess.run(
                [bbseal, f'in={p}_R#.trim.fq', f'pattern={p}_out_%_#.fq.gz', f'outu={p}_unmapped_#.fq.gz', 'ambig=all',
                 'ref=/media/graeberlab/wdgold/nbayley/refs/gencode.v31.transcripts.fa.gz,/media/graeberlab/wdgold/nbayley/refs/gencode.vM22.transcripts.fa.gz',
                 f'refstats={p}_refstats.txt', 'refnames=t', 'overwrite=t', 'k=16'])
            os.makedirs(p, exist_ok=True)
            os.remove(f'{p}_R1.trim.fq')
            os.remove(f'{p}_R2.trim.fq')
            os.rename(f'{p}_out_gencode.v31.transcripts_1.fq.gz', f'{p}/{p}_out_gencode.v31.transcripts_1.fq.gz')
            os.rename(f'{p}_out_gencode.v31.transcripts_2.fq.gz', f'{p}/{p}_out_gencode.v31.transcripts_2.fq.gz')
            os.rename(f'{p}_refstats.txt', f'{p}/{p}_refstats.txt')
            os.rename(f'{p}_out_gencode.vM22.transcripts_1.fq.gz', f'{p}/{p}_out_gencode.vM22.transcripts_1.fq.gz')
            os.rename(f'{p}_out_gencode.vM22.transcripts_2.fq.gz', f'{p}/{p}_out_gencode.vM22.transcripts_2.fq.gz')
            os.rename(f'{p}_unmapped_1.fq.gz', f'{p}/{p}_unmapped_1.fq.gz')
            os.rename(f'{p}_unmapped_2.fq.gz', f'{p}/{p}_unmapped_2.fq.gz')
