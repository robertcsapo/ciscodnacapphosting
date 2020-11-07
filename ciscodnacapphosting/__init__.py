import json
from types import SimpleNamespace as Namespace
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder
import xmltodict
from ciscodnacapphosting import dockerctl
from ciscodnacapphosting import cli


class Api:
    def __init__(self):
        self.settings = {}
        self.settings["dnac_host"] = "dnac-gotlab.aws.labrats.se"
        self.settings["dnac_user"] = "admin"
        self.settings["dnac_pass"] = "Gotlab13"
        self.settings["dnac_verify"] = True
        self.settings["dnac_token"] = None
        self.docker = dockerctl.Api()

        config = self.config(operation="read")
        self.settings = {**self.settings, **config[1]}
        #print(json.dumps(self.settings, indent=4))

        self._auth()
        return
    def config(hostname="", username="", password="", insecure="", **kwargs):
        if "write" in kwargs["operation"]:
            data = {
                "dnac": {
                    "hostname": hostname,
                    "username": username,
                    "password": password,
                    "insecure": insecure
                }
            }
            try:
                with open("config.json", "w") as f: 
                    # Writing data to a file 
                    f.write(json.dumps(data, indent=4))
                f.close()
                return True, None
            except Exception as e:
                return False, f"Can't update config file ({e})"
        if "read" in kwargs["operation"]:
            try:
                with open("config.json", "r") as f: 
                    # Writing data to a file 
                    data = f.read()
                f.close()
                return True, json.loads(data)
            except Exception as e:
                return False, f"Can't read config file ({e})"

        return False, "Error"
        
            

    def _auth(self):
        url = f"https://{self.settings['dnac_host']}/dna/system/api/v1/auth/token"
        data = self._request(type="auth", url=url)
        self.settings["dnac_token"] = data["Token"]
        pass

    def get(self, **kwargs):
        print(kwargs)
        if "image" in kwargs:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps?searchByName={kwargs['image']}"
            if "tag" in kwargs:
                url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps/{kwargs['image']}/{kwargs['tag']}"
        elif "appId" in kwargs:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/latest"
            if "tag" in kwargs:
                url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/{kwargs['tag']}"
        else:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps?limit=1000&offset=0"
        
        print(url)
        #import sys
        #sys.exit()
        data = self._request(type="get", url=url)
        return data

    def upload(self, **kwargs):
        url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps?type=docker"
        data = self._request(type="post", url=url, tar=kwargs["tar"])
        # print(data["appId"])
        if "categories" in kwargs:
            data = self.update(
                appId=data["appId"],
                tag=data["version"],
                categories=kwargs["categories"],
            )
            pass
        else:
            kwargs["categories"] = "Others"
            data = self.update(
                appId=data["appId"],
                tag=data["version"],
                categories=kwargs["categories"],
            )
        # print(data)
        return data

    def update(self, **kwargs):
        print(kwargs)
        app = self.get(appId=kwargs["appId"])
        if "tag" in kwargs:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/{kwargs['tag']}"
        else:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/latest"
        # data = {}
        valid_metadata = self._supported_app_metadata(**kwargs)
        if valid_metadata[0] is False:
            raise Exception(f"Error: Unsupported metadata for application {kwargs}")
        data = {**app, **valid_metadata[1]}
        import json

        # print(json.dumps(app, indent=4))
        # print(json.dumps(data, indent=4))
        # import sys
        # sys.exit()
        data = self._request(type="put", url=url, payload=data)
        return data

    def delete(self, **kwargs):
        if "tag" in kwargs:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/{kwargs['tag']}?cancelOutstandingActions=true"
        else:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/latest?cancelOutstandingActions=true"
        data = self._request(type="delete", url=url)
        return data

    def _supported_app_metadata(self, **kwargs):
        data = {}
        if "categories" in kwargs:
            categories = ["Monitoring", "Security", "IOT", "Others"]
            if kwargs["categories"] in categories:
                data["categories"] = []
                data["categories"].append(kwargs["categories"])
                return True, data
            return False, None

    def _update_app_info(self, id, **kwargs):
        """
        TODO REMOVE?
        """

        # https://dnac-gotlab.aws.labrats.se/api/iox/service/api/v1/appmgr/apps/8d445e1b-b707-47f6-bd8d-8a273758d389/latest
        return

    def _request(self, **kwargs):
        if "auth" in kwargs["type"].lower():
            url = kwargs["url"]
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            response = requests.request(
                "POST",
                url,
                auth=HTTPBasicAuth(
                    self.settings["dnac_user"], self.settings["dnac_pass"]
                ),
                headers=headers,
                verify=self.settings["dnac_verify"],
            )
            data = response.json()
            return data

        if "get" in kwargs["type"].lower():
            url = kwargs["url"]
            headers = {
                "X-Auth-Token": self.settings["dnac_token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, verify=self.settings["dnac_verify"]
            )
            data = response.json()
            return data
        if "post" in kwargs["type"].lower():
            """
            Make pretty TODO
            missing SSL verify
            """
            url = kwargs["url"]
            tar = kwargs["tar"]
            print(tar)
            headers = {
                "X-Auth-Token": self.settings["dnac_token"],
                "Content-Type": "multi-part/form-data",
                "Accept": "application/json",
            }
            """
            TODO
            Content-Disposition: form-data; name="file"; filename="speedtest.tar"
            Content-Type: application/x-tar
            """
            print(tar)
            # response = requests.request("POST", url, files={tar: open(tar, 'rb')}, headers=headers)

            # files = {'name': 'file', 'filename': ('speedtest.tar', open('speedtest.tar', 'rb'), 'application/x-tar')}
            # files = {'name': ('file', None), 'filename': ('speedtest.tar', open('speedtest.tar', 'rb'), 'application/x-tar')}
            # files = {"filename":"speedtest.tar","file": ("speedtest.tar", open('speedtest.tar', 'rb'), 'application/x-tar')}
            # files = {"name":"speedtest.tar", "file":"speedtest.tar" ,"filename": ("speedtest", open('speedtest.tar', 'rb'), 'application/x-tar')}

            mp_encoder = MultipartEncoder(
                fields={
                    "filename": tar,
                    "file": (tar, open(tar, "rb"), "application/x-tar"),
                }
            )
            response = requests.post(
                url,
                data=mp_encoder,
                headers={
                    "Content-Type": mp_encoder.content_type,
                    "X-Auth-Token": self.settings["dnac_token"],
                },
            )
            # files = {"name": (open('alpine.tar', 'rb')), "filename":("alpine.tar", 'application/x-tar')}
            # response = requests.post(url, files=files, headers=headers)
            # print(response.request.body)
            # print(response.request.headers)
            print(response.status_code)

            if response.ok:
                data = response.json()
            else:
                data = xmltodict.parse(response.content)
                raise Exception(
                    f"Error ({data['error']['code']}): {data['error']['description']}"
                )
            return data

        if "put" in kwargs["type"].lower():
            """
            TODO clean up
            """
            url = kwargs["url"]
            payload = json.dumps(kwargs["payload"])
            # import json
            # print("---")
            # print(json.dumps(payload, indent=4))
            headers = {
                "X-Auth-Token": self.settings["dnac_token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            response = requests.request(
                "PUT",
                url,
                headers=headers,
                data=payload,
                verify=self.settings["dnac_verify"],
            )
            print(response.status_code)
            if response.ok:
                data = response.json()
                # print(data)
            else:
                print(response.content)
                """
                TODO error at update?
                """
                return
            return data
        if "delete" in kwargs["type"].lower():
            url = kwargs["url"]
            headers = {
                "X-Auth-Token": self.settings["dnac_token"],
                "Content-Type": "application/json",
            }
            response = requests.request(
                "DELETE", url, headers=headers, verify=self.settings["dnac_verify"]
            )
            print(response.status_code)
            if response.ok:
                return True
            else:
                return False

        return
