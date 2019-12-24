from subprocess import run, PIPE
import click

project = 'thesecretaryofwar'
zone = 'us-east1-b'

def getoutput(cmd, shell=True, check=True):
    return run(
        cmd,
        shell=shell,
        check=True,
        universal_newlines=True,
        stdout=PIPE
    ).stdout

def getpods(status=None, all=True):
    all = '-a' if all else ''
    if status is None:
        ret = getoutput(
            "kubectl get pods {all} -o json | jq -r '.items[].metadata.name'".format(all=all)
        )
    else:
        ret = getoutput(
            "kubectl get pods {all} -o json | jq -r '.items[] | select(.status.phase == \"{status}\") | .metadata.name'".format(all=all, status=status)
        )
    return ret.strip().split('\n')

def getnodes():
    return getoutput("kubectl get nodes -o json | jq -r '.items[].metadata.name'").strip().split('\n')

def runall(cmd):
    for node in getnodes():
        click.echo(node)
        runnode(cmd, node)
        click.echo()

def runnode(cmd, node):
    run(
        'gcloud compute --project "{project}" ssh --zone "{zone}" "{node}" --command="{cmd}"'.format(
            cmd=cmd,
            node=node,
            project=project,
            zone=zone
        ),
        shell=True
    )

@click.group()
def cli():
    pass

@cli.group()
def nodes():
    pass

@nodes.command()
def ls():
    for node in getnodes():
        click.echo(node)

@nodes.command()
def df():
    runall("df -h | grep '/var$'")

@nodes.command()
def gc():
    runall('docker rm \$(docker ps -q -f status=exited)')

@cli.group()
def pods():
    pass

@pods.command()
def ls():
    for pod in getpods(status='Succeeded'):
        click.echo(pod)

@pods.command()
def gc():
    for pod in getpods(status='Succeeded'):
        click.echo(pod)
        run('kubectl delete pod {pod}'.format(pod=pod), shell=True)

@cli.command()
@click.argument('command')
def cmd(command):
    runall(command)

if __name__ == '__main__':
    cli()
