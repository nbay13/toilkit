#!/bin/bash
# Renames all FAIL.UUID*.tar.gz files in a folder to UUID*.tar.gz by unzipping, renaming, and rezipping
mkdir -p renamed
for file in FAIL*.tar.gz; do
	echo $file
	NEWNAME=$(echo $file | cut -f2 -d ".")
	tar -xvzf $file
	mv ${file//.tar.gz} $NEWNAME
	tar -czvf $NEWNAME".tar.gz" $NEWNAME 
	rm -r $NEWNAME
	mv $file renamed
done


