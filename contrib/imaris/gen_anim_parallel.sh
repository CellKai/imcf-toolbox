#!/bin/bash

# Poor man's multithreading via shell jobs.

MAX_JOBS=4

if ! [ -d "$1" ] ; then
    echo "Usage: $0 /path/to/csvfiles"
    exit 1
fi

#for file in $1/*/*.csv ; do 
find "$1" -type f -iname '*.csv' | while read file ; do
    (
        tgt="$(echo ${file} | sed 's,.csv$,,')"
        fname="$(echo ${tgt} | sed 's,.*/,,')"
        mkdir -pv "${tgt}-plot"
        python junction_statistics.py -i "$file" --export-plot "${tgt}-plot"
        avconv \
            -threads 1 \
            -r 10 \
            -i "${tgt}-plot/3dplot-%03d.png" \
            -c:v libx264 \
            -b:v 2000k \
            "${tgt}-plot/${fname}.mp4"
    ) &
    while [ `jobs | wc -l` -ge $MAX_JOBS ] ; do
        sleep 1
    done
done
