from requests import post, get
from os import getenv
from jwcrypto import jwt, jwk
import urllib.parse
import time


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
    user = user_response.json()

    now = int(time.time())
    key = jwk.JWK(generate='oct', size=256)
    token = jwt.JWT(header={'alg': 'HS256'},
                    claims={
                        'user_id': user['id'],
                        'username': user['login'],
                        'email': user['email']},
                    default_claims={
                        'jti': True,
                        'iss': getenv('ISSUER'),
                        'aud': getenv('ISSUER'),
                        'nbf': now,
                        'iat': now,
                        'exp': now + getenv('TOKEN_EXPIRATION_TIME')})
    token.make_signed_token(key)
    print(token.serialize())

    return oauth_json
