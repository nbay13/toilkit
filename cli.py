import argparse
from commands.fastq_merge import parse_merge_args
from commands.fastq_rename_by_key import rename_by_key
from commands.batch_bbduk_bbseal import bbduk_bbseal

def main():
    parser = argparse.ArgumentParser(prog='toilkit')
    subparsers = parser.add_subparsers()

    # Add subcommand for fastq_merge
    parser_fastq_merge = subparsers.add_parser('fastq_merge')
    parser_fastq_merge.add_argument('indir', help='Directory containing .gz files')
    parser_fastq_merge.add_argument('split_char', help='Character to split file names', default='_')
    parser_fastq_merge.add_argument('outdir', help='Output directory', default='.')
    parser_fastq_merge.add_argument('write_method', help='The method of merging (p, i, or s)', default='s')
    parser_fastq_merge.set_defaults(func=parse_merge_args)

    # Add subcommand for rename_by_key
    parser_rename_by_key = subparsers.add_parser('rename_by_key')
    parser_rename_by_key.add_argument('dir', help='The directory containing the files to rename')
    parser_rename_by_key.add_argument('pattern', help='The filename pattern to match')
    parser_rename_by_key.add_argument('keyname', help='The file name key to match')
    parser_rename_by_key.set_defaults(func=rename_by_key)

    # Add subcommand for bbduk_bbseal
    parser_bbduk_bbseal = subparsers.add_parser('bbduk_bbseal')
    parser_bbduk_bbseal.add_argument('bbdukdir', help='The directory containing bbduk.sh')
    parser_bbduk_bbseal.add_argument('bbsealdir', help='The directory containing bbseal.sh')
    parser_bbduk_bbseal.set_defaults(func=bbduk_bbseal)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
