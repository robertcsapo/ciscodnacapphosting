import json
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

@click.group(chain=True)
#@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    print('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command("dnac")
@click.pass_context
def dnac(ctx):
    pass
@cli.command("config")
@click.option('--hostname', required=False)
@click.option('--username', required=False)
@click.option('--password', required=False)
@click.option('--insecure/--no-insecure', default=False)
@click.pass_context
def dnac_config(ctx, hostname, username, password, insecure):
    status = ciscodnacapphosting.Api.config(hostname, username, password, insecure, operation="write")
    if status[0] is True:
        click.echo("Success: Config Updated")
    else:
        click.echo("Error: Config couldn't be updated")
    return

@cli.command('app')
@click.option('--id', required=False)
@click.option('--image', required=False)
@click.option('--tag', required=False)
@click.pass_context
def app(ctx, id, image, tag):
    dnac_app = ciscodnacapphosting.Api()
    click.echo('app')
    if id != None:
        if tag != None:
            print("catch")
            id = "35273d1d-4dd4-497c-9151-4bd9b2394fa8"
            tag = "3.12.1"
            app = dnac_app.get(appId=id, tag=tag)
            click.echo(json.dumps(app, indent=4))
            return
        id = "35273d1d-4dd4-497c-9151-4bd9b2394fa8"
        app = dnac_app.get(appId=id)
        click.echo(json.dumps(app, indent=4))
        return
    if image != None:
        if tag != None:
            image = "alpine"
            tag = "3.12.1"
            app = dnac_app.get(image=image, tag=tag)
            click.echo(json.dumps(app, indent=4))
            return
        image = "alpine"
        app = dnac_app.get(image=image)
        click.echo(json.dumps(app, indent=4))
        return
    apps = dnac_app.get()
    for app in apps["data"]:
        click.echo(json.dumps(app, indent=4))
    return

@cli.command()
@click.option('--download', required=False)
@click.option('--save/--no-save', default=False)
def docker(download, save):
    dnac_app = ciscodnacapphosting.Api()
    print(type(save))
    if download != None:
        docker_download = dnac_app.docker.download(image="alpine", tag="3.12.1")
        print(docker_download)
    if save is True:
        print("catch")
        save = dnac_app.docker.save(image=docker_download['image'], tag=docker_download['tag'])
    return


@cli.command()
@click.option('--settings', nargs=3, required=True)
@click.option('--insecure/--no-insecure', default=False)
@click.pass_context
def dnac2(ctx, settings, insecure):
    dnac_app = ciscodnacapphosting.Api()
    ctx.dnac_app = dnac_app
    return



if __name__ == "__main__":
    cli()
