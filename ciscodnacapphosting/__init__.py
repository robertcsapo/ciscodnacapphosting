import json
from types import SimpleNamespace as Namespace
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder
import xmltodict
from ciscodnacapphosting import dockerctl
from ciscodnacapphosting import cli

version = "0.1"


class Api:
    def __init__(self):
        self.settings = {}
        """
        self.settings["dnac_host"] = "dnac-gotlab.aws.labrats.se"
        self.settings["dnac_user"] = "admin"
        self.settings["dnac_pass"] = "Gotlab13"
        self.settings["dnac_verify"] = True
        self.settings["dnac_token"] = None
        """
        self.docker = dockerctl.Api()
        config = self.config(operation="read")
        self.settings = {**self.settings, **config[1]}

        self._auth()
        return

    def config(hostname="", username="", password="", insecure="", **kwargs):
        if "write" in kwargs["operation"]:
            data = {
                "dnac": {
                    "hostname": hostname,
                    "username": username,
                    "password": password,
                    "insecure": insecure,
                }
            }
            try:
                with open("config.json", "w") as f:
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
        url = (
            f"https://{self.settings['dnac']['hostname']}/dna/system/api/v1/auth/token"
        )
        data = self._request(type="auth", url=url)
        self.settings["dnac"]["token"] = data["Token"]
        pass

    def get(self, **kwargs):
        if "image" in kwargs:
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps?searchByName={kwargs['image']}"
            if "tag" in kwargs:
                url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['image']}/{kwargs['tag']}"
        elif "appId" in kwargs:
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/latest"
            if "tag" in kwargs:
                url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/{kwargs['tag']}"
        else:
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps?limit=1000&offset=0"
        data = self._request(type="get", url=url)
        return data

    def upload(self, **kwargs):
        url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps?type=docker"
        data = self._request(type="post", url=url, tar=kwargs["tar"])
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
        return data

    def update(self, **kwargs):
        app = self.get(appId=kwargs["appId"])
        if "tag" in kwargs:
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/{kwargs['tag']}"
        else:
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/latest"
        valid_metadata = self._supported_app_metadata(**kwargs)
        if valid_metadata[0] is False:
            raise Exception(f"Error: Unsupported metadata for application {kwargs}")
        data = {**app, **valid_metadata[1]}
        data = self._request(type="put", url=url, payload=data)
        return data

    def delete(self, **kwargs):
        if "tag" in kwargs:
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/{kwargs['tag']}?cancelOutstandingActions=true"
        else:
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/latest?cancelOutstandingActions=true"
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
        return False, None

    def _request(self, **kwargs):
        if "auth" in kwargs["type"].lower():
            url = kwargs["url"]
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            response = requests.request(
                "POST",
                url,
                auth=HTTPBasicAuth(
                    self.settings["dnac"]["username"], self.settings["dnac"]["password"]
                ),
                headers=headers,
                verify=self.settings["dnac"]["insecure"],
            )
            data = response.json()
            return data

        if "get" in kwargs["type"].lower():
            url = kwargs["url"]
            headers = {
                "X-Auth-Token": self.settings["dnac"]["token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, verify=self.settings["dnac"]["insecure"]
            )
            data = response.json()
            return data
        if "post" in kwargs["type"].lower():
            url = kwargs["url"]
            tar = kwargs["tar"]
            headers = {
                "X-Auth-Token": self.settings["dnac"]["token"],
                "Content-Type": "multi-part/form-data",
                "Accept": "application/json",
            }
            multi_part = MultipartEncoder(
                fields={
                    "filename": tar,
                    "file": (tar, open(tar, "rb"), "application/x-tar"),
                }
            )
            response = requests.request(
                "POST",
                url,
                data=multi_part,
                headers={
                    "Content-Type": multi_part.content_type,
                    "X-Auth-Token": self.settings["dnac"]["token"],
                },
                verify=self.settings["dnac"]["insecure"],
            )
            if response.ok:
                data = response.json()
            else:
                data = xmltodict.parse(response.content)
                raise Exception(
                    f"Error ({data['error']['code']}): {data['error']['description']}"
                )
            return data

        if "put" in kwargs["type"].lower():
            url = kwargs["url"]
            payload = json.dumps(kwargs["payload"])
            headers = {
                "X-Auth-Token": self.settings["dnac"]["token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            response = requests.request(
                "PUT",
                url,
                headers=headers,
                data=payload,
                verify=self.settings["dnac"]["insecure"],
            )
            if response.ok:
                data = response.json()
            else:
                raise Exception(f"Error: Problem to update app - {response.content}")
            return data
        if "delete" in kwargs["type"].lower():
            url = kwargs["url"]
            headers = {
                "X-Auth-Token": self.settings["dnac"]["token"],
                "Content-Type": "application/json",
            }
            response = requests.request(
                "DELETE", url, headers=headers, verify=self.settings["dnac"]["insecure"]
            )
            print(response.status_code)
            if response.ok:
                return True
            else:
                return False

        return
