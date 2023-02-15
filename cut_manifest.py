import argparse
import os

def split_file(manifest_file, split_num):
    with open(manifest_file, 'r') as f:
        lines = f.readlines()

    num_files = len(lines)
    for i in range(num_files):
        ext = os.path.splitext(manifest_file)[1]
        base = os.path.splitext(manifest_file)[0]
        with open(f"{base}-{i+1}{ext}", 'w') as f:
            f.writelines(lines[i * split_num: (i + 1) * split_num])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest_file', help='Manifest File to split')
    parser.add_argument('split_num', type=int, help='Number of lines per split file')
    args = parser.parse_args()

    split_file(args.manifest_file, args.split_num)
