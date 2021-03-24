from requests import post
from os import getenv
import urllib.parse


def authenticate(client_id, code):
    payload = {
        "client_id": client_id,
        "client_secret": getenv("CLIENT_SECRET"),
        "code": code
    }
    response = post('https://github.com/login/oauth/access_token', params=payload)
    response_json = urllib.parse.parse_qs(response.text)
    return response_json
