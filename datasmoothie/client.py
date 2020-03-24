import json
import requests

HOST = "www.datasmoothie.com/api2/"

class Client:
    def __init__(self, api_key):
        self.__api_key = api_key

    def _get_headers(self):
        return {"Authorization": "Token {}".format(self.__api_key)}

    def request(self, resource, action=None):
        base_url = "https://{}".format(HOST)
        if action is None:
            action=""
        result = requests.get("{}/{}/{}".format(base_url, resource, action), headers=self._get_headers())
        result = json.loads(result.content)
        return result
