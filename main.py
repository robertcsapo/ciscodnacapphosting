import ciscodnacapphosting

if __name__ == "__main__":
    import logging
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.info("Starting Application")
    dnac_app = ciscodnacapphosting.Api()
    
    download = dnac_app.docker.download(image="busybox", tag="1.31")
    save = dnac_app.docker.save(image=download["image"], tag=download["tag"])
    upload = dnac_app.upload(tar=save["filename"], categories="IOT")
    app = dnac_app.get(appId=upload["appId"])
    print(f'Name: {app["name"]}\tAppId: {app["appId"]}')
    #delete = dnac_app.delete(appId=upload["appId"])
    

    """
    download = dnac_app.docker.download(image="busybox", tag="1.32")
    save = dnac_app.docker.save(image=download["image"], tag=download["tag"])
    app = dnac_app.get(image="busybox")
    appId = app["data"][0]["appId"]
    #upgrade = dnac_app.upgrade(appId=appId, tag="1.31", tar="busybox-1.32.tar", categories="IOT")
    upgrade = dnac_app.upgrade(appId=appId, tar="busybox-1.32.tar", categories="IOT")
    app = dnac_app.get(appId=upgrade["appId"])
    delete = dnac_app.delete(appId=upgrade["appId"], tag="1.32")
    """
  
    
    """
    download = dnac_app.docker.download(image="nginx", tag="latest")
    save = dnac_app.docker.save(image=download["image"], tag=download["tag"])
    upload = dnac_app.upload(tar=save["filename"], categories="IOT")

    apps = dnac_app.get()
    for app in apps["data"]:
        print(f"Name: {app['name']}\tAppId: {app['appId']}")

    update = dnac_app.update(appId="46e54562-83c9-4183-8632-c597c8cc5a2b", categories="IOT")
    
    app = dnac_app.get(image="robertcsapo/speedtest")
    print(f'Name: {app["data"][0]["name"]}\tAppId: {app["data"][0]["appId"]}')
    app = dnac_app.get(appId="46e54562-83c9-4183-8632-c597c8cc5a2b")
    print(f'Name: {app["name"]}\tAppId: {app["appId"]}')

    delete = dnac_app.delete(appId=upload["appId"])
    print(f'Deleted\tAppId: {upload["appId"]}')
    """
