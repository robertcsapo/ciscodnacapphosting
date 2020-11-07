
import ciscodnacapphosting
'''
import docker
client = docker.from_env()

def docker_download(image="", tag="latest"):
    client = docker.from_env()
    print(client)

    images = client.images.list()

    print(images)

    pull = client.images.pull('nginx', '1.10-alpine')

    print(pull)
    return

def docker_save(image="", tag="latest"):
    image = client.images.get("nginx:1.10-alpine")
    f = open('./nginx-1.10-alpine.tar', 'wb')
    for chunk in image.save():
        f.write(chunk)
    f.close()
    return
'''
#r = requests.post(url, files={tarFile: open(tarFile, 'rb')}, headers=headers)

dnac_app = ciscodnacapphosting.Api()
dnac_app.docker
dnac_app.docker.download(image="alpine")
#dnac_app.docker.download()

dnac_app.docker.save(image="alpine", tag="latest")

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
