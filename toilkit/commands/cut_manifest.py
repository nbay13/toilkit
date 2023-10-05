import os

def cut_manifest(args):
    split_num = args.split_num
    manifest_file = args.manifest_file
    with open(manifest_file, 'r') as f:
        lines = f.readlines()

    num_files = len(lines)
    for i in range(0, num_files, split_num):
        ext = os.path.splitext(manifest_file)[1]
        base = os.path.splitext(manifest_file)[0]
        with open(f"{base}-{i//split_num+1}{ext}", 'w') as f:
            f.writelines(lines[i:i + split_num])
