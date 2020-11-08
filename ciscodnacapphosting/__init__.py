import json
import logging
from types import SimpleNamespace as Namespace
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder
import xmltodict
from ciscodnacapphosting import dockerctl
from ciscodnacapphosting import cli
import base64

version = "0.1"

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

class Api:
    def __init__(self):
        self.settings = {}
        self.docker = dockerctl.Api()
        config = self.config(operation="read")
        self.settings = {**self.settings, **config[1]}

        self._auth()
        return

    def config(hostname="", username="", password="", secure="", **kwargs):
        if "encode" in kwargs["operation"]:
            data = {
                "dnac": {
                    "hostname": hostname,
                    "username": username,
                    "password": password,
                    "secure": secure,
                }
            }
            data = str(data)
            #data_bytes = data.encode('ascii')
            data_base64 = base64.b64encode(data.encode("ascii"))
            #print("catch")
            print(data_base64.decode("utf-8"))
            #import sys
            #sys.exit()
            try:
                with open("config.json", "w") as f:
                    f.write(data_base64.decode("utf-8"))
                f.close()
                return True, None
            except Exception as e:
                return False, f"Can't update config file ({e})"
            pass
        if "decode" in kwargs["operation"]:
            pass
        if "write" in kwargs["operation"]:
            data = {
                "dnac": {
                    "hostname": hostname,
                    "username": username,
                    "password": password,
                    "secure": secure,
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
                raise Exception(f"Can't read config file ({e})")

        return False, "Error"

    def _auth(self):
        url = (
            f"https://{self.settings['dnac']['hostname']}/dna/system/api/v1/auth/token"
        )
        logging.info(f"Cisco DNA Center Authentication ({url})")
        data = self._request(type="auth", url=url)
        self.settings["dnac"]["token"] = data["Token"]
        return

    def get(self, **kwargs):
        if "image" in kwargs:
            logging.info(f"Cisco DNA Center AppHosting App ({kwargs['image']})")
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps?searchByName={kwargs['image']}"
            if "tag" in kwargs:
                url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['image']}/{kwargs['tag']}"
        elif "appId" in kwargs:
            logging.info(f"Cisco DNA Center AppHosting App ({kwargs['appId']})")
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/latest"
            if "tag" in kwargs:
                url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/{kwargs['tag']}"
        else:
            logging.info(f"Cisco DNA Center AppHosting App List")
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps?limit=1000&offset=0"
        
        data = self._request(type="get", url=url)
        return data

    def upload(self, **kwargs):
        url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps?type=docker"
        logging.info(f"Cisco DNA Center AppHosting Upload ({kwargs['tar']})")
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
        logging.info(f"Cisco DNA Center AppHosting Update App ({data['name']})")
        data = self._request(type="put", url=url, payload=data)
        return data

    def delete(self, **kwargs):
        if "tag" in kwargs:
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/{kwargs['tag']}?cancelOutstandingActions=true"
        else:
            url = f"https://{self.settings['dnac']['hostname']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/latest?cancelOutstandingActions=true"
        logging.info(f"Cisco DNA Center AppHosting Delete App ({kwargs['appId']})")
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
                verify=self.settings["dnac"]["secure"],
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
                "GET", url, headers=headers, verify=self.settings["dnac"]["secure"]
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
                verify=self.settings["dnac"]["secure"],
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
                verify=self.settings["dnac"]["secure"],
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
                "DELETE", url, headers=headers, verify=self.settings["dnac"]["secure"]
            )
            if response.ok:
                return True
            else:
                return False

        return
