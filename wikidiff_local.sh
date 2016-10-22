#!/usr/bin/bash

INPATH=$HOME/work/docker/data
OUTPATH=$HOME/work/docker/output
TEMP=$HOME/tmp

DATE=20160901
EXT=7z
UNZIP="7z x"
INFILE=enwiki-$DATE-pages-meta-history$1.xml-$2
OUTFILE=enwiki-$DATE-diff-$1-$2.csv

echo "starting"

echo "unzipping wiki history"
$UNZIP -o $TEMP $INPATH/$INFILE.$EXT

echo "parsing wiki history"
python3 wikidiff_fast.py $TEMP/$INFILE $OUTPATH/$OUTFILE

if [ $? -eq 0 ]; then
    echo "parse succeeded"
else
    echo "parse failed"
fi

echo "removing files"
rm $TEMP/$INFILE

echo "done"
