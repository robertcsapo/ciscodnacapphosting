import ciscodnacapphosting

if __name__ == "__main__":
    """ Start logging if you want more details """
    import logging

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Start Application")

    """ Instance of ciscodnacapphosting """
    dnac_app = ciscodnacapphosting.Api()

    """
    Docker API
    """

    """ Download Image """
    download = dnac_app.docker.download(image="busybox", tag="1.31")
    print(f"Image: {download['image']} Tag: {download['tag']}")
    """ Save image as tar file """
    save = dnac_app.docker.save(image=download["image"], tag=download["tag"])
    print(f"Image: {save['image']} Tag: {save['tag']} Filename: {save['filename']}")
    """ Filename == repo_image-tag.tar """

    """
    Cisco DNA Center App Hosting APIs
    """

    """ Get current Apps """
    apps = dnac_app.get()
    for app in apps["data"]:
        print(f"Name: {app['name']}\tAppId: {app['appId']}")

    """ Search for app """
    app = dnac_app.get(image="busybox")
    for app in apps["data"]:
        print(f"Name: {app['name']}\tTag: app['version']\tAppId: {app['appId']}")

    """ Upload App """
    upload = dnac_app.upload(tar=save["filename"], categories="IOT")
    print(f'Name: {upload["name"]}\tAppId: {upload["appId"]}')
    app = dnac_app.get(appId=upload["appId"])
    print(f'Name: {app["name"]}\tAppId: {app["appId"]}')

    """ Upgrade App """
    download = dnac_app.docker.download(image="busybox", tag="1.32")
    save = dnac_app.docker.save(image=download["image"], tag=download["tag"])
    app = dnac_app.get(image="busybox")
    appId = app["data"][0]["appId"]
    tag = app["data"][0]["version"]
    upgrade = dnac_app.upgrade(
        appId=appId, tag=tag, tar="busybox-1.32.tar", categories="IOT"
    )
    print(f"New AppId {upgrade['appId']} of {upgrade['name']}:{upgrade['version']}")

    """ Update App Metadata """
    update = dnac_app.update(
        appId="46e54562-83c9-4183-8632-c597c8cc5a2b", categories="IOT"
    )
    print(f"Update App ({update['appId']}) {update['name']} - categories")

    """ Delete App """
    app = dnac_app.get(image="busybox")
    appId = app["data"][0]["appId"]
    tag = app["data"][0]["version"]
    delete = dnac_app.delete(appId=appId, tag=tag)
    print(f"Deleted\tAppId: {appId}")
