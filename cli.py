import ciscodnacapphosting
import click

"""
@click.command()
@click.option('--docker', is_flag=True, help="Will print verbose messages.")
@click.option('--verbose', is_flag=True, help="Will print verbose messages.")
@click.option('--name', default='', help='Who are you?')
def docker(verbose,name):
    if verbose:
        click.echo("We are in the verbose mode.")
    click.echo("Hello World")
    click.echo('Bye {0}'.format(name))
"""

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    print('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
@click.option('--download', required=False)
@click.option('--save/--no-save', default=False)
def docker(download, save):
    print(f'Synching {download}')
    print(type(save))
    if download != None:
        docker_download = dnac_app.docker.download(image="alpine", tag="3.12.1")
        print(docker_download)
    if save is True:
        print("catch")
        save = dnac_app.docker.save(image=docker_download['image'], tag=docker_download['tag'])

if __name__ == "__main__":
    dnac_app = ciscodnacapphosting.Api()
    cli()
