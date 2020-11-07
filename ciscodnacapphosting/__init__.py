import json
from types import SimpleNamespace as Namespace
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.multipart.encoder import MultipartEncoder
import xmltodict

class Api:
    def __init__(self):
        self.settings = {}
        self.settings["dnac_host"] = "dnac-gotlab.aws.labrats.se"
        self.settings["dnac_user"] = "admin"
        self.settings["dnac_pass"] = "Gotlab13"
        self.settings["dnac_verify"] = True
        self.settings["dnac_token"] = None

        self._auth()
        return

    def _auth(self):
        url = f"https://{self.settings['dnac_host']}/dna/system/api/v1/auth/token"
        data = self._request(type="auth", url=url)
        self.settings["dnac_token"] = data["Token"]
        pass

    def get(self, **kwargs):
        if "image" in kwargs:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps?searchByName={kwargs['image']}"
        else:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps?limit=1000&offset=0"
        print(kwargs)
        data = self._request(type="get", url=url)
        return data

    def upload(self, **kwargs):
        url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps?type=docker"
        data = self._request(type="post", url=url, tar=kwargs["tar"])
        return data

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        if "tag" in kwargs:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/{kwargs['tag']}?cancelOutstandingActions=true"
        else:
            url = f"https://{self.settings['dnac_host']}/api/iox/service/api/v1/appmgr/apps/{kwargs['appId']}/latest?cancelOutstandingActions=true"
        data = self._request(type="delete", url=url)
        return data

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
            """ Make pretty TODO """
            url = kwargs["url"]
            tar = kwargs["tar"]
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


            #files = {'name': 'file', 'filename': ('speedtest.tar', open('speedtest.tar', 'rb'), 'application/x-tar')}
            #files = {'name': ('file', None), 'filename': ('speedtest.tar', open('speedtest.tar', 'rb'), 'application/x-tar')}
            #files = {"filename":"speedtest.tar","file": ("speedtest.tar", open('speedtest.tar', 'rb'), 'application/x-tar')}
            #files = {"name":"speedtest.tar", "file":"speedtest.tar" ,"filename": ("speedtest", open('speedtest.tar', 'rb'), 'application/x-tar')}

            mp_encoder = MultipartEncoder(
                fields={
                    'filename': tar,
                    'file': (tar, open(tar, 'rb'), 'application/x-tar'),
                }
            )
            response = requests.post(url, data=mp_encoder, headers={'Content-Type': mp_encoder.content_type, "X-Auth-Token": self.settings["dnac_token"]})
            #files = {"name": (open('alpine.tar', 'rb')), "filename":("alpine.tar", 'application/x-tar')}
            #response = requests.post(url, files=files, headers=headers)
            #print(response.request.body)
            #print(response.request.headers)
            print(response.status_code)

            if response.ok:
                data = response.json()
            else:
                data = xmltodict.parse(response.content)
                raise Exception(f"Error ({data['error']['code']}): {data['error']['description']}")
            return data

        if "put" in kwargs["type"].lower():
            url = kwargs["url"]
            payload = kwargs["payload"]
            headers = {
                "X-Auth-Token": self.settings["dnac_token"],
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            """
            TODO
            Content-Disposition: form-data; name="file"; filename="speedtest.tar"
            Content-Type: application/x-tar
            """
            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=payload,
                verify=self.settings["dnac_verify"],
            )
            data = response.json()
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

    def parse(data):
        return json.loads(json.dumps(data), object_hook=event)
