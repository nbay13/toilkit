import glob
import os
import argparse

# TODO: upgrade to argparser
  #e.g. usage: python fastq_rename_by_key.py /media/graeberlab/My\ Book/RNA\ Batch\ 14/ "*.fastq.gz" RNA14\ Index\ simple.txt
  #For argparse: python fastq_rename_by_key.py /path/to/directory "*.fastq.gz" keyfile.txt
  #With argparse, this can be done in any order, just need --keyname or --pattern before the first argument


def rename_by_key(args):
  direc = args.dir
  pattern = args.pattern
  keyname = args.keyname
  # TODO: change to arg
  split_char = "_R"
  print("Directory: " + direc)
  print("Filename pattern: " + pattern)
  print("Filename key: " + keyname)

  os.chdir(direc)
  filenames = [f for f in glob.glob(pattern)]
  # initalize a dictionary
  d = {}
  # open the file and start reading lines
  with open(keyname) as f:
    # we don't need the first line, but we can store it as a list if we want
    # header = [l.rstrip() for l in f.readline().split('\t')]
    for line in f:
      # split the string by tabs into a list,
      # iterate over the list and remove the newline special character,
      # set first entry to 'key' and second entry to 'val'
      key, val = [l.rstrip() for l in line.split('\t')]
      # add tuple variables to dict
      d[key] = val
  print(d)
  # split the filenames by "_" and save as list
  # filesnames is a list of all the original full file names
  ids = [filename.split(split_char)[0] for filename in filenames]
  # access values in the dict based on filename ids and save as list
  # iterate through list of first part of original file names and create new list with the corresponding corrected first part of file names using the key
  new_ids = [d[id] for id in ids]
  suffixes = [split_char.join(filename.split(split_char)[1:]) for filename in filenames]
  # add original filename suffixes to dict values in the list
  new_filenames = [split_char.join((new_id, suffix)) for new_id, suffix in zip(new_ids, suffixes)]
  # use os.rename to rename the files using the 'filenames' list and the 'new_filenames' list
  for filename, new_filename in zip(filenames, new_filenames):
    os.rename(filename, new_filename)
