# import os
# import shutil

# def concatenate_fastq(input_file1, input_file2, output_file):
#     with open(input_file1, 'rb') as f1, open(input_file2, 'rb') as f2, open(output_file, 'wb') as out_file:
#         shutil.copyfileobj(f1, out_file)
#         shutil.copyfileobj(f2, out_file)

# def cat_bbseal(args):
#     for f in os.listdir(args.dir):
#         if os.path.isdir(f):
#             os.chdir(f)
#             print(f)
#             concatenate_fastq(f + "_out_gencode.v31.transcripts_1.fq.gz", f + "_unmapped_1.fq.gz", f + "_human_ambig_umap_reads_R1.fq.gz")
#             concatenate_fastq(f + "_out_gencode.v31.transcripts_2.fq.gz", f + "_unmapped_2.fq.gz", f + "_human_ambig_umap_reads_R2.fq.gz")
#             os.chdir("..")
import subprocess

def cat_bbseal(args):
    # use bash script b/c cat faster for larger files
    bash_script = f"""
    for f in {args.dir}/*/; do
        f=${{f%*/}}
        cd $f
        echo $f
        cat ${{f}}_out_gencode.v31.transcripts_1.fq.gz ${{f}}_unmapped_1.fq.gz > ${{f}}_human_ambig_umap_reads_R1.fq.gz
        cat ${{f}}_out_gencode.v31.transcripts_2.fq.gz ${{f}}_unmapped_2.fq.gz > ${{f}}_human_ambig_umap_reads_R2.fq.gz
        cd ..
    done
    """
    subprocess.run(["bash", "-c", bash_script], check=True)
