import os

src = 'history'
dst = 'history_new'

# run = print
run = os.system

targs = []
for fn0 in os.listdir(src):
    tag, _ = os.path.splitext(fn0)
    if not os.path.isfile(f'{dst}/{tag}.bz2'):
        targs.append(tag)

for tag in sorted(targs):
    print(f'extracting  {tag}')
    run(f'lrunzip -o {dst}/{tag} {src}/{tag}.lrz')
    print(f'compressing {tag}')
    run(f'pbzip2 -p8 {dst}/{tag}')
