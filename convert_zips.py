# convert to lrzip

import os

hist_file = 'history_list_20160901.txt'

fnames = [s.strip() for s in open(hist_file)]

os.chdir('data')

for f in fnames[6:]:
    print(f)
    os.system('7z x %s.7z' % f)
    os.system('lrzip -f %s' % f)
    os.system('rm %s' % f)
    print()

os.chdir('..')
