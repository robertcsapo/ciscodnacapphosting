import requests
from requests.auth import HTTPBasicAuth


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
        data = self._request(type="get", url=url)
        return data

    def upload(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def _request(self, **kwargs):
        if "auth" in kwargs["type"]:
            url = kwargs["url"]
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            response = requests.request(
                "POST",
                url,
                auth=HTTPBasicAuth(self.settings["dnac_user"], self.settings["dnac_pass"]),
                headers=headers,
                verify=self.settings["dnac_verify"],
            )
            data = response.json()
            return data

        if "get" in kwargs["type"]:
            url = kwargs["url"]
            headers = {
                "x-auth-token": self.settings["dnac_token"],
                "Content-Type": "application/json",
            }
            response = requests.request(
                "GET", url, headers=headers, verify=self.settings["dnac_verify"]
            )
            data = response.json()
            return data
        return
