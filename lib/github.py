from requests import post, get
from os import getenv
import urllib.parse


def authenticate(client_id, code):
    payload = {
        "client_id": client_id,
        "client_secret": getenv("CLIENT_SECRET"),
        "code": code
    }
    oauth_response = post(
        'https://github.com/login/oauth/access_token', params=payload)
    oauth_json = urllib.parse.parse_qs(oauth_response.text)

    user_response = get('https://api.github.com/user',
                        headers={'Authorization': 'token ' + oauth_json['access_token'][0]})
    print(user_response.json())
    return oauth_json
