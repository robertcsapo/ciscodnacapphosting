
import ciscodnacapphosting

if __name__ == "__main__":
    dnac_app = ciscodnacapphosting.Api()

    """
    download = dnac_app.docker.download(image="alpine", tag="3.12.1")
    print(f"Download: {download}")
    save = dnac_app.docker.save(image=download['image'], tag=download['tag'])
    print(f"Save: {save}")
    upload = dnac_app.upload(tar=save["filename"], categories="IOT")
    print(f"Upload: {upload['name']}")
    """

    """
    download = dnac_app.docker.download(image="busybox", tag="1.32.0-glibc")
    print(f"Image: {download")
    #dnac_app.docker.download()
    save = dnac_app.docker.save(image=download['image'], tag=download['tag'])
    print(f"Save: {save}")
    #dnac_app.docker.save(image="alpine", tag="latest")
    """

    """
    apps = dnac_app.get()
    for app in apps["data"]:
        print(app["appId"])
        #import json
        #print(json.dumps(app, indent=4))

    update = dnac_app.update(appId="46e54562-83c9-4183-8632-c597c8cc5a2b", categories="IOT")
    print(update)
    """

    """
    upload = dnac_app.upload(tar="alpine.tar", categories="IOT")
    #upload = dnac_app.upload(tar="speedtest.tar")
    print(upload["appId"])
    delete = dnac_app.delete(appId=upload["appId"])
    """

    """
    #print(dnac_app.settings)
    #print(dnac_app.get())
    #print(dnac_app.get(image="robertcsapo/speedtest"))
    app = dnac_app.get(image="robertcsapo/speedtest")
    print(f'AppId: {app["data"][0]["appId"]} - Name: {app["data"][0]["name"]}')
    app_id = app["data"][0]["appId"]
    delete = dnac_app.delete(appId=app_id)
    print(delete)
    """
