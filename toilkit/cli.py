import argparse
from .commands.fastq_merge import parse_merge_args
from .commands.fastq_rename_by_key import rename_by_key
from .commands.batch_bbduk_bbseal import bbduk_bbseal
from .commands.cat_bbseal_output import cat_bbseal
from .commands.make_manifest import make_manifest
from .commands.manifest_2_anno_v2 import manifest_to_anno
from .commands.cut_manifest import cut_manifest
from .commands.gather_bbseal_metrics import gather_bbseal_metrics
from .commands.rename_toil_output import rename_toil_output
from .commands.batch_rename_TOIL_FAIL import batch_rename_TOIL_FAIL
from .commands.process_uuid_tars import process_uuid_tars

def main():
    parser = argparse.ArgumentParser(prog='toilkit')
    subparsers = parser.add_subparsers()

    # Add subcommand for fastq_merge
    parser_fastq_merge = subparsers.add_parser('fastq_merge')
    parser_fastq_merge.add_argument('--indir', nargs='?', help='Directory containing .gz files', default='.')
    parser_fastq_merge.add_argument('--split_char', nargs='?', help='Character to split file names', default='_')
    parser_fastq_merge.add_argument('--outdir', nargs='?', help='Output directory', default='.')
    parser_fastq_merge.add_argument('--write_method', nargs='?', help='The method of merging (p, i, or s)', default='s')
    parser_fastq_merge.set_defaults(func=parse_merge_args)

    # Add subcommand for rename_by_key
    parser_rename_by_key = subparsers.add_parser('rename_by_key')
    parser_rename_by_key.add_argument('--dir', nargs='?', help='The directory containing the files to rename', default = '.')
    parser_rename_by_key.add_argument('--pattern', nargs='?', help='The filename pattern to match', default = '*.fastq.gz')
    parser_rename_by_key.add_argument('--keyname', help='The file name key to match')
    parser_rename_by_key.set_defaults(func=rename_by_key)

    # Add subcommand for bbduk_bbseal
    parser_bbduk_bbseal = subparsers.add_parser('bbduk_bbseal')
    parser_bbduk_bbseal.add_argument('--bbduk_dir', help='The directory containing bbduk.sh')
    parser_bbduk_bbseal.add_argument('--ref_genome_dir', help='The directory containing the reference genome .gz files')
    parser_bbduk_bbseal.set_defaults(func=bbduk_bbseal)

    # Add subcommand for cat_bbseal
    parser_cat_bbseal = subparsers.add_parser('cat_bbseal')
    parser_cat_bbseal.add_argument('--dir', nargs='?', help='The directory containing bbseal results', default='.')
    parser_cat_bbseal.set_defaults(func=cat_bbseal)

    # Add subcommand for make_manifest
    parser_make_manifest = subparsers.add_parser('make_manifest')
    parser_make_manifest.add_argument('--dir', nargs='?', help="The working directory", default='.')
    parser_make_manifest.add_argument('--tdir', nargs= '?', help="The target directory of the fastqs", default='.')
    parser_make_manifest.add_argument('--suffix', nargs='?', default='.tsv', help="The suffix of the manifest file (ex. nathanson-15-1.tsv)")
    parser_make_manifest.add_argument('--starting_num', nargs='?', default=0, type=int,
                        help="a number for each pair of fastq files listed in the manifest file")
    parser_make_manifest.set_defaults(func=make_manifest)

    # Add subcommand for manifest_to_anno
    parser_manifest_to_anno = subparsers.add_parser('manifest_to_anno')
    parser_manifest_to_anno.add_argument('--infile', required=True, help='The input manifest file')
    parser_manifest_to_anno.add_argument('--outfile', help='The output annotation file', default = 'idkey.txt')
    parser_manifest_to_anno.set_defaults(func=manifest_to_anno)

    # Add subcommand for cut_manifest
    parser_cut_manifest = subparsers.add_parser('cut_manifest')
    parser_cut_manifest.add_argument('--manifest_file', required=True, help='Manifest File to split')
    parser_cut_manifest.add_argument('--split_num', type=int, required=True, help='Number of lines per split file')
    parser_cut_manifest.set_defaults(func=cut_manifest)

    # Add subcommand for gather_bbseal_metrics
    parser_gather_bbseal_metrics = subparsers.add_parser('gather_bbseal_metrics')
    parser_gather_bbseal_metrics.add_argument('--dir', nargs='?', help='The directory of the bbseal results',
                        default='.')
    parser_gather_bbseal_metrics.add_argument('--outfile', nargs='?', help='The prefix of the output file', default='toilkit-bbseal')
    parser_gather_bbseal_metrics.set_defaults(func=gather_bbseal_metrics)

    # Add subcommand for rename_toil_output
    parser_rename_toil_output = subparsers.add_parser('rename_toil_output')
    parser_rename_toil_output.add_argument('--infile', type=str, help='Path to the input txt file')
    parser_rename_toil_output.add_argument('--direction', type=int, choices=[1, 2], help='Direction of renaming (1 or 2)', default = 1)
    parser_rename_toil_output.set_defaults(func=rename_toil_output)

    #Add subcommand for batch_rename_TOIL_FAIL
    parser_batch_rename_TOIL_FAIL = subparsers.add_parser('batch_rename_TOIL_FAIL')
    parser_batch_rename_TOIL_FAIL.add_argument('--indir', nargs = '?', default = '.', help='The directory containing the files to rename')
    parser_batch_rename_TOIL_FAIL.set_defaults(func=batch_rename_TOIL_FAIL)

    #Add subcommand for 2uuid_parser
    parser_process_uuid_tars = subparsers.add_parser('process_uuid_tars')
    parser_process_uuid_tars.add_argument('--prefix', nargs = '?', help='The output filenames prefix', default = 'toilkit-output')
    parser_process_uuid_tars.add_argument('--anno_filename', nargs = '?', help='The annotation file', default = 'idkey.txt')
    parser_process_uuid_tars.add_argument('--indir', nargs = '?', help='The input path of annotation data', default = '.')
    parser_process_uuid_tars.add_argument('--omit_rsem', action='store_true', help='Include this flag to omit rsem')
    parser_process_uuid_tars.add_argument('--omit_bamqc', action='store_true', help='Include this flag to omit bamqc')
    parser_process_uuid_tars.add_argument('--omit_collate_qc', action='store_true', help='Include this flag to omit QC')
    parser_process_uuid_tars.add_argument('--omit_star_junctions', action='store_true', help='Include this flag to omit star junctions')
    parser_process_uuid_tars.add_argument('--star_output',
                                                       help='The output path of where to put the star junctions data',
                                                       default='junctions/', nargs = '?')
    parser_process_uuid_tars.set_defaults(func=process_uuid_tars)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
