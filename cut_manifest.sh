#!/usr/bin/env bash
manifest_file=$1
split_num=$2
manifest_ext='.'"${1##*.}"
filename="${1%.*}"
split -d -l $split_num -a 1 $manifest_file $filename'.' --additional-suffix $manifest_ext
