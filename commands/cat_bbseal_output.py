import os
def cat_bbseal(args):
    for f in os.listdir(args.dir):
        if os.path.isdir(f):
            os.chdir(f)
            print(f)
            with open(f + "_human_ambig_umap_reads_R1.fq.gz", "w") as outfile:
                outfile.write(open(f + "_out_gencode.v31.transcripts_1.fq.gz").read())
                outfile.write(open(f + "_unmapped_1.fq.gz").read())
            with open(f + "_human_ambig_umap_reads_R2.fq.gz", "w") as outfile:
                outfile.write(open(f + "_out_gencode.v31.transcripts_2.fq.gz").read())
                outfile.write(open(f + "_unmapped_2.fq.gz").read())
            os.chdir("..")
