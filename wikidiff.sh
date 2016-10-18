#!/usr/bin/bash

KEYFILE=/etc/secret-volume/ssh-privatekey
SCP_OPTS="-o StrictHostKeyChecking=no"
USER=doug
SERVER=dohan.dyndns.org

INPATH=work/docker/data
OUTPATH=work/docker/output

DATE=20160901
EXT=lrz
UNZIP="lrunzip"
INFILE=enwiki-$DATE-pages-meta-history$1.xml-$2
OUTFILE=enwiki-$DATE-diff-$1-$2.csv

echo "starting"

echo "copying file to server"
scp $SCP_OPTS -i $KEYFILE $USER@$SERVER:$INPATH/$INFILE.$EXT .

echo "unzipping wiki history"
$UNZIP $INFILE.$EXT

echo "parsing wiki history"
python3 wikidiff_fast.py --log=parser.log $INFILE $OUTFILE

if [ $? -eq 0 ]
    echo "copying output back home"
    scp $SCP_OPTS -i $KEYFILE $OUTFILE $USER@$SERVER:$OUTPATH/
    echo "done"
    exit 0
else
    echo "parse failed"
    exit 1
fi
