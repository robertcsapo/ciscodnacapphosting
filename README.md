# cisco-dnac-app-hosting-import-docker-images
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/robertcsapo/ciscodnacapphosting)
![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/robertcsapo/ciscodnacapphosting)
![Docker Pulls](https://img.shields.io/docker/pulls/robertcsapo/ciscodnacapphosting)
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/robertcsapo/ciscodnacapphosting)  
![PyPI - Downloads](https://img.shields.io/pypi/dm/ciscodnacapphosting)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/ciscodnacapphosting)
![PyPI](https://img.shields.io/pypi/v/ciscodnacapphosting)



Disclaimer  
This solution leverages currently unpublished Cisco DNA Center APIs (as of DATE)  
Do not use in production

```ciscodnacapphosting``` is a Python SDK for Cisco DNA Center Application Hosting API.  
It uses local docker environment to pull and save docker images.

# Prerequisites
- Cisco DNA Center
  - Supported release: 2.1.2+
- Cisco Catalyst 9000 Switches/APs
- Python
  - Version: 3.8+

# Demo
```bash
ciscodnacapphosting app --image busybox
Get App (busybox)
data:
- _links:
    configuration:
      href: /api/v1/appmgr/apps/71257f4a-1f68-43a5-85f0-3347137107bb/1.32/config
    icon:
      href: null
    images:
      href: /api/v1/appmgr/apps/71257f4a-1f68-43a5-85f0-3347137107bb/1.32/images
    packages:
      href: /api/v1/appmgr/apps/71257f4a-1f68-43a5-85f0-3347137107bb/1.32/packages
    self:
      href: /api/v1/appmgr/apps/71257f4a-1f68-43a5-85f0-3347137107bb/1.32
  appId: 71257f4a-1f68-43a5-85f0-3347137107bb
  appType: docker
  categories:
  - IOT
  classification: APP
  cpuUsage: 0
  description:
    contentType: text
  descriptor:
    app:
      cpuarch: x86_64
      env:
        PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      resources:
        network:
        - interface-name: eth0
          ports: {}
        profile: c1.large
      startup:
        rootfs: fogd_upload_8699102144278681062.tar
        target:
        - sh
      type: docker
    descriptor-schema-version: '2.2'
    info:
      name: busybox
      version: '1.32'
  icon:
    caption: icon
    href: null
  images: []
  lastUpdatedDate: 1604930943165
  localAppId: 71257f4a-1f68-43a5-85f0-3347137107bb
  memoryUsage: 0
  name: busybox
  packages:
  - href: /api/v1/appmgr/apps/71257f4a-1f68-43a5-85f0-3347137107bb/1.32/packages/b55be543-b969-415b-b47d-da95df834a5f
  profileNeeded: c1.large
  properties: []
  published: true
  releaseNotes:
    contentType: text
  services: []
  signed: false
  version: '1.32'
```
```bash
ciscodnacapphosting docker --download alpine:3.12.0 --save
Download completed (alpine) - saved as alpine-3.12.0.tar
```
```bash
ciscodnacapphosting upload --file alpine-3.12.0.tar --categories IOT
Upload App (alpine-3.12.0.tar) - IOT
New AppId (1a12b3d9-22d5-40ee-8aff-e2ccfb79c59f) alpine:3.12.0 - IOT
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ```ciscodnacapphosting```.

```bash
pip install ciscodnacapphosting
```

## Usage

Configuration can be stored in config.json in JSON format.
```
{
    "dnac": {
        "hostname": "dnac.example.tld",
        "username": "superadmin",
        "password": "superpassword",
        "secure": true
    }
}
```
_(secure parameter is for HTTPS verification)_

The configuration can be encoded as base64 string.
```ewogICAgImRuYWMiOiB7CiAgICAgICAgImhvc3RuYW1lIjogImRuYWMuZXhhbXBsZS50bGQiLAogICAgICAgICJ1c2VybmFtZSI6ICJzdXBlcmFkbWluIiwKICAgICAgICAicGFzc3dvcmQiOiAic3VwZXJwYXNzd29yZCIsCiAgICAgICAgInNlY3VyZSI6IHRydWUKICAgIH0KfQ==```

If using base64 encoded, then it's possible to set Environment ```DNAC_CONFIG```
```bash
export DNAC_CONFIG=ewogICAgImRuYWMiOiB7CiAgICAgICAgImhvc3RuYW1lIjogImRuYWMuZXhhbXBsZS50bGQiLAogICAgICAgICJ1c2VybmFtZSI6ICJzdXBlcmFkbWluIiwKICAgICAgICAicGFzc3dvcmQiOiAic3VwZXJwYXNzd29yZCIsCiAgICAgICAgInNlY3VyZSI6IHRydWUKICAgIH0KfQ==
```

### CLI

```bash
ciscodnacapphosting config --hostname dnac.example.tld --username superadmin --password superpassword --secure --encode

ciscodnacapphosting app
ciscodnacapphosting app--image busybox

ciscodnacapphosting docker
ciscodnacapphosting docker --download busybox:1.31 --save

ciscodnacapphosting upload --file busybox-1.31.tar --categories IOT

ciscodnacapphosting upgrade --id 71257f4a-1f68-43a5-85f0-3347137107bb --tag 1.31 --file busybox-1.32.tar --categories IOT

ciscodnacapphosting update --id 71257f4a-1f68-43a5-85f0-3347137107bb --categories Security

ciscodnacapphosting delete --id 71257f4a-1f68-43a5-85f0-3347137107bb --tag 1.31
```

#### Help
```bash
ciscodnacapphosting --help
Usage: ciscodnacapphosting [OPTIONS] COMMAND1 [ARGS]... [COMMAND2
                           [ARGS]...]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  app
  config
  delete
  docker
  update
  upgrade
  upload
  whoami
  ```

### Include in Python

```python
import ciscodnacapphosting

dnac_app = ciscodnacapphosting.Api()
download = dnac_app.docker.download(image="busybox", tag="1.31")
save = dnac_app.docker.save(image=download["image"], tag=download["tag"])
upload = dnac_app.upload(tar=save["filename"], categories="IOT")
upgrade = dnac_app.upgrade(
        appId=appId, tag=tag, tar="busybox-1.32.tar", categories="IOT"
    )
update = dnac_app.update(
        appId="46e54562-83c9-4183-8632-c597c8cc5a2b", categories="IOT"
    )
delete = dnac_app.delete(appId=appId, tag=tag)
```
_(More examples in [examples/](./examples) folder)_

### Docker
```docker
docker run -it --rm --privileged -e DNAC_CONFIG=ewogICAgImRuYWMiOiB7CiAgICAgICAgImhvc3RuYW1lIjogImRuYWMuZXhhbXBsZS50bGQiLAogICAgICAgICJ1c2VybmFtZSI6ICJzdXBlcmFkbWluIiwKICAgICAgICAicGFzc3dvcmQiOiAic3VwZXJwYXNzd29yZCIsCiAgICAgICAgInNlY3VyZSI6IHRydWUKICAgIH0KfQ== robertcsapo/ciscodnacapphosting
```
```bash
/ # ciscodnacapphosting whoami
Config: {"dnac": {"hostname": "dnac.example.tld", "username": "superadmin", "password": "superpassword", "secure": true}}
/ # 
```
```bash
/ # ciscodnacapphosting app --image alpine
Get App (alpine)
data:
- _links:
    configuration:
      href: /api/v1/appmgr/apps/1a12b3d9-22d5-40ee-8aff-e2ccfb79c59f/3.12.0/config
    icon:
      href: null
    images:
      href: /api/v1/appmgr/apps/1a12b3d9-22d5-40ee-8aff-e2ccfb79c59f/3.12.0/images
    packages:
      href: /api/v1/appmgr/apps/1a12b3d9-22d5-40ee-8aff-e2ccfb79c59f/3.12.0/packages
    self:
      href: /api/v1/appmgr/apps/1a12b3d9-22d5-40ee-8aff-e2ccfb79c59f/3.12.0
  appId: 1a12b3d9-22d5-40ee-8aff-e2ccfb79c59f
  appType: docker
  categories:
  - IOT
  classification: APP
  cpuUsage: 0
  creationDate: 1604950418368
  description:
    contentType: text
  descriptor:
    app:
      cpuarch: x86_64
      env:
        PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
      resources:
        network:
        - interface-name: eth0
          ports: {}
        profile: c1.large
      startup:
        rootfs: fogd_upload_7626901429300115262.tar
        target:
        - /bin/sh
      type: docker
    descriptor-schema-version: '2.2'
    info:
      name: alpine
      version: 3.12.0
  icon:
    caption: icon
    href: null
  images: []
  localAppId: 1a12b3d9-22d5-40ee-8aff-e2ccfb79c59f
  memoryUsage: 0
  name: alpine
  packages:
  - href: /api/v1/appmgr/apps/1a12b3d9-22d5-40ee-8aff-e2ccfb79c59f/3.12.0/packages/10d8de54-9c21-4f65-bda1-540ef5e4e1ac
  profileNeeded: c1.large
  properties: []
  published: true
  releaseNotes:
    contentType: text
  services: []
  signed: false
  version: 3.12.0
```

## Technologies & Frameworks Used

**Cisco Products & Services:**

- [Cisco DNA Center Platform API](https://developer.cisco.com/dnacenter/)
- [Docker](https://www.docker.com/get-started)
    - [dockerpy](https://github.com/docker/docker-py/)

## Authors & Maintainers

- Robert Csapo <rcsapo@cisco.com>

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
