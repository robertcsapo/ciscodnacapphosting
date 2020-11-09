import os
import json
import click
import yaml
import ciscodnacapphosting


"""ciscodnacapphosting  Console Script.
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

""" Main Entry """


@click.group(chain=True)
@click.version_option()
@click.pass_context
def cli(ctx):
    pass


""" Display current config """


@cli.command("whoami")
@click.pass_context
def dnac_config(ctx):
    if "DNAC_CONFIG" in os.environ:
        config = ciscodnacapphosting.Api.config(
            config=os.environ["DNAC_CONFIG"], operation="decode"
        )
        click.echo(f"Config: {json.dumps(config[1])}")
        return
    else:
        config = ciscodnacapphosting.Api.config(operation="read")
        click.echo(f"Config: {config[1]}")
        return


""" Configures Cisco DNA Center settings """


@cli.command("config")
@click.option("--hostname", required=True)
@click.option("--username", required=True)
@click.option("--password", required=True)
@click.option("--secure/--insecure", default=True)
@click.option("--encode/--no-decode", default=False)
@click.pass_context
def dnac_config(ctx, hostname, username, password, secure, encode):
    if encode is True:
        config = ciscodnacapphosting.Api.config(
            hostname, username, password, secure, operation="encode"
        )
    else:
        config = ciscodnacapphosting.Api.config(
            hostname, username, password, secure, operation="write"
        )
    if config[0] is True:
        click.echo("Success: Config Updated")
        if encode is True:
            click.echo(f"Config Encode: {config[1]}")
    else:
        click.echo("Error: Config couldn't be updated")
    return


""" Get Application(s) from Cisco DNA Center """


@cli.command("app")
@click.option("--id", required=False)
@click.option("--image", required=False)
@click.option("--tag", required=False)
@click.pass_context
def app(ctx, id, image, tag):
    dnac_app = ciscodnacapphosting.Api()
    if id != None:
        click.echo(f"Get App ({id})")
        if tag != None:
            app = dnac_app.get(appId=id, tag=tag)
            click.echo(
                yaml.safe_dump(app, allow_unicode=True, default_flow_style=False)
            )
            return
        app = dnac_app.get(appId=id)
        click.echo(yaml.safe_dump(app, allow_unicode=True, default_flow_style=False))
        return
    if image != None:
        click.echo(f"Get App ({image})")
        if tag != None:
            app = dnac_app.get(image=image, tag=tag)
            click.echo(
                yaml.safe_dump(app, allow_unicode=True, default_flow_style=False)
            )
            return
        app = dnac_app.get(image=image)
        click.echo(yaml.safe_dump(app, allow_unicode=True, default_flow_style=False))
        return
    click.echo(f"Get App list")
    apps = dnac_app.get()
    for app in apps["data"]:
        click.echo(yaml.safe_dump(app, allow_unicode=True, default_flow_style=False))
    return


""" Upload Applications to Cisco DNA Center """


@cli.command("upload")
@click.option("--file", required=True)
@click.option("--categories", required=True)
@click.pass_context
def upload(ctx, file, categories):
    dnac_app = ciscodnacapphosting.Api()
    click.echo(f"Upload App ({file}) - {categories}")
    upload = dnac_app.upload(tar=file, categories=categories)
    click.echo(
        f"New AppId ({upload['appId']}) {upload['name']}:{upload['version']} - {categories}"
    )
    return


""" Upgrade Applications to Cisco DNA Center """


@cli.command("upgrade")
@click.option("--id", required=True)
@click.option("--tag", required=False)
@click.option("--file", required=True)
@click.option("--categories", required=True)
@click.pass_context
def upgrade(ctx, id, tag, file, categories):
    dnac_app = ciscodnacapphosting.Api()
    if tag != None:
        click.echo(f"Upgrade App ({file}) - {tag} - {categories}")
        upgrade = dnac_app.upgrade(appId=id, tag=tag, tar=file, categories=categories)
    else:
        click.echo(f"Upgrade App ({file}) - latest - {categories}")
        upgrade = dnac_app.upgrade(appId=id, tar=file, categories=categories)
    click.echo(
        f"New AppId {upgrade['appId']} of {upgrade['name']}:{upgrade['version']}"
    )
    return


""" Update Metadata about Applications to Cisco DNA Center """


@cli.command("update")
@click.option("--id", required=True)
@click.option("--categories", required=True)
@click.pass_context
def update(ctx, id, categories):
    dnac_app = ciscodnacapphosting.Api()
    click.echo(f"Update App ({id}) - {categories}")
    update = dnac_app.update(appId=id, categories=categories)
    click.echo(f"Update App ({update['appId']}) {update['name']} - categories")
    return


""" Delete Application(s) from Cisco DNA Center """


@cli.command("delete")
@click.option("--id", required=True)
@click.option("--tag", required=False)
@click.pass_context
def delete(ctx, id, tag):
    dnac_app = ciscodnacapphosting.Api()
    if tag != None:
        click.echo(f"Delete App ({id}) - {tag}")
        delete = dnac_app.delete(appId=id, tag=tag)
        click.echo(f"Deleted App ({id}) - {tag}")
    else:
        click.echo(f"Delete App ({id})")
        delete = dnac_app.delete(appId=id)
        click.echo(f"Deleted App ({id})")
    return


""" Wrapped docker cli to download and save """


@cli.command("docker")
@click.option("--download", required=False)
@click.option("--save/--no-save", default=False)
def docker(download, save):
    dnac_app = ciscodnacapphosting.Api()
    if download == None and save is False:
        download = click.prompt("Docker image")
        save = True
        click.echo(f"Downloading {download} and saving it locally")
    if download != None:
        if ":" in download:
            download = download.split(":")
            docker_download = dnac_app.docker.download(
                image=download[0], tag=download[1]
            )
        else:
            docker_download = dnac_app.docker.download(image=download, tag="latest")
    if save is True:
        save = dnac_app.docker.save(
            image=docker_download["image"], tag=docker_download["tag"]
        )
        click.echo(
            f"Download completed ({save['image']}) - saved as {save['filename']}"
        )
    return


if __name__ == "__main__":
    cli()
