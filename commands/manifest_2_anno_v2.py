import sys
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('input', help='The input manifest file')
parser.add_argument('output', help='The output annotation file')

args = parser.parse_args()
input_file = args.input
output_file = args.output

# Clear output file and add header in preparation for appending
with open(output_file, 'w') as out:
    out.write("uuid\tsample\n")

print("processing manifest file: " + input_file)

# iterate over each line (with check for EOF), unless that line is empty
with open(input_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # echo without quotes around variable automatically converts tabs (in original file) to spaces, hence the space delimiter
        uuid = line.split("\t")[2]

        # remove all directory info, get the name of file
        temp = os.path.basename(line)
        # remove first underscore and everything after
        id = temp.split("_")[0]

        with open(output_file, 'a') as out:
            out.write(uuid + "\t" + id + "\n")
