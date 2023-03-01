#!/usr/bin/env python 
'''
Author: Nick Bayley
Last edited: 11/18/2021
Description: A script for gathering junction data from TOIL STAR output and renaming the files based on an annotation file.
'''
import sys
import os
import glob
import tarfile
import zipfile
import re

anno_filename = 'annotation.tmp.txt'
input_path = ''
output_path = 'junctions/'

if len(input_path) > 0:
	if input_path[-1] != "/":
		sys.exit("Error: Need forward slash at the end of input path")

if len(output_path) > 0:
	if output_path[-1] != "/":
		sys.exit("Error: Need forward slash at the end of output path")

if not os.path.isdir(output_path):
	print("\nCreating output folder: %s" % (output_path))
	os.mkdir(output_path)

print("\nGathering TOIL STAR junction data with " + anno_filename + "\n")
anno_dict = {}
with open(anno_filename, "r") as anno:
	header = next(anno)
	for line in anno:
		uuid=line.split('\t')[0].strip()
		samplename=str(line.split('\t')[1]).strip()
		anno_dict[uuid]=samplename

folders = glob.glob(input_path + 'UUID_[0-9]*.tar.gz')
toil_ids = [os.path.basename(dir).rsplit('.')[0] for dir in folders]
if any([id not in anno_dict.keys() for id in toil_ids]):
	sys.exit("Error: Missing UUID annotations")

for i, dir in enumerate(folders):
	print('...Accessing %s (%d/%d)' % (dir, i+1, len(toil_ids)))
	with tarfile.open(dir) as tar:
		files = tar.getnames()
		junction_filename = filter(lambda x: re.search('SJ.out.tab', x), files)[0]
		file = tar.extractfile(junction_filename)
		lines = file.readlines()
		print('...Writing STAR junction file to: %s\n' % ('.'.join([anno_dict[toil_ids[i]], 'SJ.out.tab'])))
		with open('%s%s.SJ.out.tab' % (output_path, anno_dict[toil_ids[i]]), 'w') as output:
			for line in lines:
				output.write(line)

print("All Done! Renamed SJ.out.tab files can be found at: %s" % (output_path))


		

		




