import re
import os
import sys
import argparse
import subprocess as sub
from subprocess import PIPE
from multiprocessing import Pool

parser = argparse.ArgumentParser(description='parallel compressed wikidiff indexer')
parser.add_argument('indir', type=str, help='directory of files to index')
parser.add_argument('outdir', type=str, help='directory to output to')
parser.add_argument('--threads', type=int, default=10, help='number of threads to use')
parser.add_argument('--output', type=int, default=100, help='log output rate')
args = parser.parse_args()

def index_file(fname):
    fbase, _ = os.path.splitext(fname)
    fin = f'{args.indir}/{fname}'
    fout = f'{args.outdir}/{fbase}.csv'

    if os.path.exists(fout):
        print(f'File exists: {fname}')
        return
    else:
        print(f'Parsing: {fname}')

    proc = sub.Popen(f'bzcat {fin} | grep -n "<title>"', shell=True, stdout=PIPE)
    outp = open(fout, 'w+')
    outp.write('line,title\n')

    for i, data in enumerate(proc.stdout):
        if len(data) == 0:
            break

        line = data.decode().rstrip()
        if not ret := re.match('(\d+): +<title>(.+)</title>', line):
            continue

        num, title = ret.groups()
        outp.write(f'{num},"{title}"\n')

        if i % args.output == 0:
            print(f'[{i:>10}] {num:>15} -> {title}')

    outp.close()

file_list = sorted(os.listdir(args.indir))
with Pool(args.threads) as pool:
    pool.map(index_file, file_list, chunksize=1)
