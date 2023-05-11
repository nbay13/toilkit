#!/usr/bin/env bash
{
	direction=$2
	read 
	while IFS=$'\t' read -r -a p || [ -n "$p" ]
	do
		if [ $direction == '1' ]
		then
			orig=${p[0]}
			new=${p[1]}
		else
			new=${p[0]}
			orig=${p[1]}
		fi	
		tar -xvzf $orig".tar.gz"
		mv $orig $new
		tar -czvf $new".tar.gz" $new
		rm -r $new
		rm -r $orig".tar.gz"
		mv $orig".sortedByCoord.md.bam" $new".sortedByCoord.md.bam"
	done 
} < $1
