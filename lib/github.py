from requests import post, get
from os import getenv
from jwcrypto import jwt, jwk
import urllib.parse
import time

token_expiration_time = int(getenv('TOKEN_EXPIRATION_TIME'))
client_secret = getenv("CLIENT_SECRET")
issuer = getenv('ISSUER')

key_file = open('private_key.pem', 'rb')
priv_key = key_file.read()
key_file.close()

key = jwk.JWK()
key.import_from_pem(priv_key, password=None)


def authenticate(client_id, code):
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code
    }
    oauth_response = post(
        'https://github.com/login/oauth/access_token', params=payload)
    oauth_json = urllib.parse.parse_qs(oauth_response.text)

    github_token = oauth_json['access_token'][0]
    user_response = get('https://api.github.com/user',
                        headers={'Authorization': 'token ' + github_token})
    user = user_response.json()

    now = int(time.time())
    token = jwt.JWT(header={'typ': 'JWT', 'alg': 'RS512'},
                    claims={
                        'user_id': user['id'],
                        'username': user['login'],
                        'email': user['email'],
                        'github_token': github_token},
                    default_claims={
                        'jti': True,
                        'iss': issuer,
                        'aud': issuer,
                        'nbf': now,
                        'iat': now,
                        'exp': now + token_expiration_time})
    token.make_signed_token(key)

    return {
        'github_token': github_token,
        'repoadopt_token': token.serialize()
    }
