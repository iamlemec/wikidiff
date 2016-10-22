# enqueue jobs

import os
import re
import time
import jinja2
import argparse
from subprocess import check_output

parser = argparse.ArgumentParser(description='wikidiff job scheduler.')
parser.add_argument('--tag', type=str, default=None, help='id of job to queue')
parser.add_argument('--file', type=str, default=None, help='path to list of tags')
parser.add_argument('--template', type=str, default='wikidiff.yaml', help='template for job file')
parser.add_argument('--jobfile', type=str, default='jobs/tempjob.yaml', help='name of temporary jobfile')
parser.add_argument('--n', type=int, default=1, help='number of jobs to queue')
parser.add_argument('--delay', type=int, default=60, help='delay between job starts')
args = parser.parse_args()

if args.file is not None:
    tags = [s.strip() for s in open(args.file)]
elif args.tag is not None:
    tags = [args.tag]

template = jinja2.Template(open(args.template).read())

ids = [re.match(r'enwiki-(\d{8})-pages-meta-history(\d{1,2})\.xml-(p\d{9}p\d{9})', t).groups() for t in tags]

pods = [b.decode() for b in check_output("kubectl get pods -a | tail -n +2 | egrep '(Running|Pending|Complete)' | cut -d' ' -f 1", shell=True).split()]

n = 0
for (date, i1, i2) in ids:
    print(date, i1, i2)

    outfile = 'enwiki-%s-diff-%s-%s.csv' % (date, i1, i2)
    jobname = 'wikidiff-%s-%s' % (i1, i2)

    if os.path.exists(os.path.join('output', outfile)):
        print('output %s exists, skipping' % outfile)
        print()
        continue

    if jobname in pods:
        print('pod %s running or completed, skipping' % jobname)
        print()
        continue

    jobyaml = template.render(id1=i1, id2=i2)
    with open(args.jobfile, 'w') as fout:
        fout.write(jobyaml)

    os.system('kubectl create -f %s' % args.jobfile)
    print()

    n += 1
    if n >= args.n:
        break

    time.sleep(args.delay)
