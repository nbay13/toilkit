#!/bin/bash
# Reorganizes information from manifest file into annotation file to be used with post-TOIL processing aggregation
input=$1
output=$2
# Clear output file and add header in preparation for appending
echo -e "uuid"\\t"sample" > $output
echo "processing manifest file: "$input
# iterate over each line (with check for EOF), unless that line is empty
while read line || [ -n "$line" ] && [ "$line" != "" ]; do
	# skip lines beginning with hash symbol
	[ ${line:0:1} == '#' ] && continue
	# echo without quotes around variable automatically converts tabs (in orginal file) to spaces, hence the space delimiter
	uuid=$(echo $line | cut -f3 -d " ")
	# change as necessary
	#id=$(echo $line | cut -f6 -d " " | xargs basename | cut -f1 -d "_")
	# remove all directory info, get the name of file
	temp=${line##*/}
	# remove first underscore and everything after
	id=${temp%%_*}
	echo -e "$uuid"\\t"$id" >> $output
done < "${input}"	
