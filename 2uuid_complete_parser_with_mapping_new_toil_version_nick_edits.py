import tarfile
from collections import defaultdict
import collections
import os
import argparse
import pandas as pd
import itertools

prefix="LTa_xenograft"
anno_file = "annotation.tmp.txt"
min_id = 0

AnnoDict = collections.OrderedDict()
with open(anno_file, "r") as anno: #create dictionary that relates uuid to annotation name
	next(anno) #skip header
	for line in anno:
		uuid=str(line.split('\t')[0])           
                print(uuid)
		name=str(line.split('\t')[1]).rstrip()
		AnnoDict[uuid]=name


##########
#raw genes
##########

output_to_write =defaultdict(list)
headings_list = ["gene"]

def test_file_range(filename,index):
    try:
        open("UUID_"+ str(index) + ".tar.gz");
        return True
    except IOError:
	    return False

gene_list =[]
duplicate_genes =[]
gene_list_renamed =[]
'''
todo: make check outside loop, consider changing value renaming but keep for now
'''
for i in range(min_id,min_id+2):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/Hugo/rsem_genes.hugo.results')
        content = file_new.readlines()[1:]
        for line in content:
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            gene_list.append(newer_line[0])
            value = gene_list.count(newer_line[0])
            if value == 1:
                gene_list_renamed.append(newer_line[0])
            if value >= 2:
                new_name = newer_line[0] + "." + str(value)
                gene_list_renamed.append(new_name)
    break
print("Modified gene_id for all duplicates.")

for i in range(min_id,99999999):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    if test_file_range(file_name,i) == False:
        if test_file_range(file_name, i+1) == True:
	        continue
        else:
            break
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/Hugo/rsem_genes.hugo.results')
        content = file_new.readlines()[1:]
        heading= "UUID_" + str(i)
        headings_list.append(heading)
        for name, line in zip(gene_list_renamed,content):
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            output_to_write[name].append(newer_line[4])   #this is where you change it to 4
    print("Completed "+ str(i) + " file(s).")

sorted_output_to_write = sorted(output_to_write.items())

with open(prefix + "_" + "rsem_genes_raw_counts.txt", "w") as output:
    for item in headings_list:
        output.write(item +'\t')
    output.write("\n")
    for line in sorted_output_to_write:
        line_new = "\t".join(line[1])
        if line[0] == 'gene':
            continue

        output.write(line[0]+"\t" + line_new +"\n")

with open(prefix + "_" + "rsem_genes_raw_counts.txt", "r") as output:
	content =output.readlines()
with open(prefix + "_" + "rsem_genes_raw_counts.txt", "w") as output:
	head=content[0].rstrip("\n\t").split("\t")
	new_head=head[0]
	for word in head[1:]:
		new_head='\t'.join([new_head,AnnoDict[word]])
	output.write(new_head + '\n')
	for line in content[1:]:
		output.write(line)
genes=pd.read_table(prefix + "_" + "rsem_genes_raw_counts.txt", sep='\t')
genes.sort_values(by='gene',inplace=True)
genes.to_csv(prefix + "_" + "rsem_genes_raw_counts.txt",sep='\t',index=False)



################
#raw hugo transcripts
################
output_to_write =defaultdict(list)
headings_list = ["gene"]


gene_list =[]
duplicate_genes =[]
gene_list_renamed =[]
for i in range(min_id, min_id+2):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/Hugo/rsem_isoforms.hugo.results')
        content = file_new.readlines()[1:]
        for line in content:
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            gene_list.append(newer_line[0])
            value = gene_list.count(newer_line[0])
            if value == 1:
                gene_list_renamed.append(newer_line[0])
            if value >= 2:
                new_name = newer_line[0] + "." + str(value)
                gene_list_renamed.append(new_name)
    break
print("Modified gene_id for all duplicates.")

for i in range(min_id,99999999):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    if test_file_range(file_name, i) == False:
        if test_file_range(file_name, i+1) == True:
	        continue
        else:
	        break
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/Hugo/rsem_isoforms.hugo.results')
        content = file_new.readlines()[1:]
        heading= "UUID_" + str(i)
        headings_list.append(heading)
        for name, line in zip(gene_list_renamed,content):
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            output_to_write[name].append(newer_line[4])
    print("Completed "+ str(i) + " file(s).")

sorted_output_to_write = sorted(output_to_write.items())

with open(prefix + "_" + "rsem_transcripts_hugo_raw_counts.txt", "w") as output:
    for item in headings_list:
        output.write(item +'\t')
    output.write("\n")
    for line in sorted_output_to_write:
        line_new = "\t".join(line[1])
        if line[0] == 'gene':
            continue

        output.write(line[0]+"\t" + line_new +"\n")


with open(prefix + "_" + "rsem_transcripts_hugo_raw_counts.txt", "r") as output:
	content =output.readlines()
with open(prefix + "_" + "rsem_transcripts_hugo_raw_counts.txt", "w") as output:
	head=content[0].rstrip("\n\t").split("\t")
	new_head=head[0]
	for word in head[1:]:
		new_head='\t'.join([new_head,AnnoDict[word]])
	output.write(new_head + '\n')
	for line in content[1:]:
		output.write(line)
isoforms=pd.read_table(prefix + "_" + "rsem_transcripts_hugo_raw_counts.txt", sep='\t')
isoforms.sort_values(by='gene',inplace=True)
isoforms.to_csv(prefix + "_" + "rsem_transcripts_hugo_raw_counts.txt",sep='\t',index=False)



################
#raw transcripts
################

#infile: /RSEM/rsem_isoforms.results
#out:
output_to_write =defaultdict(list)
headings_list = ["gene"]


gene_list =[]
duplicate_genes =[]
gene_list_renamed =[]
for i in range(min_id,min_id+2):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/rsem_isoforms.results')
        content = file_new.readlines()[1:]
        for line in content:
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            gene_list.append(newer_line[0])
            value = gene_list.count(newer_line[0])
            if value == 1:
                gene_list_renamed.append(newer_line[0])
            if value >= 2:
                new_name = newer_line[0] + "." + str(value)
                gene_list_renamed.append(new_name)
    break
print("Modified gene_id for all duplicates.")

for i in range(min_id,99999999):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    if test_file_range(file_name, i) == False:
        if test_file_range(file_name, i+1) == True:
	        continue
        else:
	        break
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/rsem_isoforms.results')
        content = file_new.readlines()[1:]
        heading= "UUID_" + str(i)

        headings_list.append(heading)
        for name, line in zip(gene_list_renamed,content):
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            output_to_write[name].append(newer_line[4])
    print("Completed "+ str(i) + " file(s).")

sorted_output_to_write = sorted(output_to_write.items())

with open(prefix + "_" + "rsem_transcripts_raw_counts.txt", "w") as output:
    for item in headings_list:
        output.write(item +'\t')
    output.write("\n")
    for line in sorted_output_to_write:
        line_new = "\t".join(line[1])
        if line[0] == 'gene':
            continue

        output.write(line[0]+"\t" + line_new +"\n")


with open(prefix + "_" + "rsem_transcripts_raw_counts.txt", "r") as output:
	content =output.readlines()
with open(prefix + "_" + "rsem_transcripts_raw_counts.txt", "w") as output:
	head=content[0].rstrip("\n\t").split("\t")
	new_head=head[0]
	for word in head[1:]:
		new_head='\t'.join([new_head,AnnoDict[word]])
	output.write(new_head + '\n')
	for line in content[1:]:
		output.write(line)
isoforms=pd.read_table(prefix + "_" + "rsem_transcripts_raw_counts.txt", sep='\t')
isoforms.sort_values(by='gene',inplace=True)
isoforms.to_csv(prefix + "_" + "rsem_transcripts_raw_counts.txt",sep='\t',index=False)


##########
#tpm genes
##########
#in /RSEM/Hugo/rsem_genes.hugo.results
#out rsem_genes_tpm_counts.txt

output_to_write =defaultdict(list)
headings_list = ["gene"]



gene_list =[]
duplicate_genes =[]
gene_list_renamed =[]
for i in range(min_id, min_id+2):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/Hugo/rsem_genes.hugo.results')
        content = file_new.readlines()[1:]
        for line in content:
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            gene_list.append(newer_line[0])
            value = gene_list.count(newer_line[0])
            if value == 1:
                gene_list_renamed.append(newer_line[0])
            if value >= 2:
                new_name = newer_line[0] + "." + str(value)
                gene_list_renamed.append(new_name)
    break
print("Modified gene_id for all duplicates.")

for i in range(min_id,99999999):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    if test_file_range(file_name, i) == False:
        if test_file_range(file_name, i+1) == True:
	        continue
        else:
	        break
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/Hugo/rsem_genes.hugo.results')
        content = file_new.readlines()[1:]
        heading= "UUID_" + str(i)
        headings_list.append(heading)
        for name, line in zip(gene_list_renamed,content):
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            output_to_write[name].append(newer_line[5])   #this is where you change it to 5
    print("Completed "+ str(i) + " file(s).")

sorted_output_to_write = sorted(output_to_write.items())

with open(prefix + "_" + "rsem_genes_tpm_counts.txt", "w") as output:
    for item in headings_list:
        output.write(item +'\t')
    output.write("\n")
    for line in sorted_output_to_write:
        line_new = "\t".join(line[1])
        if line[0] == 'gene':
            continue

        output.write(line[0]+"\t" + line_new +"\n")

with open(prefix + "_" + "rsem_genes_tpm_counts.txt", "r") as output:
	content =output.readlines()
with open(prefix + "_" + "rsem_genes_tpm_counts.txt", "w") as output:
	head=content[0].rstrip("\n\t").split("\t")
	new_head=head[0]
	for word in head[1:]:
		new_head='\t'.join([new_head,AnnoDict[word]])
	output.write(new_head + '\n')
	for line in content[1:]:
		output.write(line)
genes=pd.read_table(prefix + "_" + "rsem_genes_tpm_counts.txt", sep='\t')
genes.sort_values(by='gene',inplace=True)
genes.to_csv(prefix + "_" + "rsem_genes_tpm_counts.txt",sep='\t',index=False)



################
#tpm hugo transcripts
################
output_to_write =defaultdict(list)
headings_list = ["gene"]



gene_list =[]
duplicate_genes =[]
gene_list_renamed =[]
for i in range(min_id, min_id+2):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/Hugo/rsem_isoforms.hugo.results')
        content = file_new.readlines()[1:]
        for line in content:
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            gene_list.append(newer_line[0])
            value = gene_list.count(newer_line[0])
            if value == 1:
                gene_list_renamed.append(newer_line[0])
            if value >= 2:
                new_name = newer_line[0] + "." + str(value)
                gene_list_renamed.append(new_name)
    break
print("Modified gene_id for all duplicates.")

for i in range(min_id,99999999):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    if test_file_range(file_name, i) == False:
        if test_file_range(file_name, i+1) == True:
	        continue
        else: 
	        break
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/Hugo/rsem_isoforms.hugo.results')
        content = file_new.readlines()[1:]
        heading= "UUID_" + str(i)
        headings_list.append(heading)
        for name, line in zip(gene_list_renamed,content):
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            output_to_write[name].append(newer_line[5])
    print("Completed "+ str(i) + " file(s).")

sorted_output_to_write = sorted(output_to_write.items())

with open(prefix + "_" + "rsem_transcripts_hugo_tpm_counts.txt", "w") as output:
    for item in headings_list:
        output.write(item +'\t')
    output.write("\n")
    for line in sorted_output_to_write:
        line_new = "\t".join(line[1])
        if line[0] == 'gene':
            continue

        output.write(line[0]+"\t" + line_new +"\n")


with open(prefix + "_" + "rsem_transcripts_hugo_tpm_counts.txt", "r") as output:
	content =output.readlines()
with open(prefix + "_" + "rsem_transcripts_hugo_tpm_counts.txt", "w") as output:
	head=content[0].rstrip("\n\t").split("\t")
	new_head=head[0]
	for word in head[1:]:
		new_head='\t'.join([new_head,AnnoDict[word]])
	output.write(new_head + '\n')
	for line in content[1:]:
		output.write(line)
isoforms=pd.read_table(prefix + "_" + "rsem_transcripts_hugo_tpm_counts.txt", sep='\t')
isoforms.sort_values(by='gene',inplace=True)
isoforms.to_csv(prefix + "_" + "rsem_transcripts_hugo_tpm_counts.txt",sep='\t',index=False)


################
#tpm transcripts
################
output_to_write =defaultdict(list)
headings_list = ["gene"]



gene_list =[]
duplicate_genes =[]
gene_list_renamed =[]
for i in range(min_id,min_id+2):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/rsem_isoforms.results')
        content = file_new.readlines()[1:]
        for line in content:
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            gene_list.append(newer_line[0])
            value = gene_list.count(newer_line[0])
            if value == 1:
                gene_list_renamed.append(newer_line[0])
            if value >= 2:
                new_name = newer_line[0] + "." + str(value)
                gene_list_renamed.append(new_name)
    break
print("Modified gene_id for all duplicates.")

for i in range(min_id,99999999):	###
    file_name = "UUID_"+ str(i) + ".tar.gz"
    if i == 0 and test_file_range(file_name,i) == False:
        continue
    if test_file_range(file_name, i) == False:
        if test_file_range(file_name, i+1) == True:
	        continue
        else: 
	        break
    with tarfile.open(file_name) as file:
        file_new = file.extractfile('UUID_'+str(i) + '/RSEM/rsem_isoforms.results')
        content = file_new.readlines()[1:]
        heading= "UUID_" + str(i)
        headings_list.append(heading)
        for name, line in zip(gene_list_renamed,content):
            new_line = bytes.decode(line)
            newer_line = new_line.rstrip("\n").split("\t")
            output_to_write[name].append(newer_line[5])
    print("Completed "+ str(i) + " file(s).")

sorted_output_to_write = sorted(output_to_write.items())

with open(prefix + "_" + "rsem_transcripts_tpm_counts.txt", "w") as output:
    for item in headings_list:
        output.write(item +'\t')
    output.write("\n")
    for line in sorted_output_to_write:
        line_new = "\t".join(line[1])
        if line[0] == 'gene':
            continue

        output.write(line[0]+"\t" + line_new +"\n")


with open(prefix + "_" + "rsem_transcripts_tpm_counts.txt", "r") as output:
	content =output.readlines()
with open(prefix + "_" + "rsem_transcripts_tpm_counts.txt", "w") as output:
	head=content[0].rstrip("\n\t").split("\t")
	new_head=head[0]
	for word in head[1:]:
		new_head='\t'.join([new_head,AnnoDict[word]])
	output.write(new_head + '\n')
	for line in content[1:]:
		output.write(line)
isoforms=pd.read_table(prefix + "_" + "rsem_transcripts_tpm_counts.txt", sep='\t')
isoforms.sort_values(by='gene',inplace=True)
isoforms.to_csv(prefix + "_" + "rsem_transcripts_tpm_counts.txt",sep='\t',index=False)


