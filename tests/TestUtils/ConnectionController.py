import json

import requests

URL = "http://127.0.0.1:8000"


def http_get(resource: str):
    response = requests.get(url=f"{URL}/{resource}",
                            headers={"Content-Type": "application/json"})
    return response


def http_post(resource: str, payload: {}):
    response = requests.post(url=f"{URL}/{resource}",
                             headers={"Content-Type": "application/json"},
                             data=json.dumps(payload))
    return response
