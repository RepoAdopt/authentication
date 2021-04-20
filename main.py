from time import sleep
from requests import post
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv

load_dotenv()

from lib.github import authenticate


app = Flask(__name__)
CORS(app)

MAX_RETRIES = 20


def establish_gateway_connection(attempts=0):
    base_url = f'http://{getenv("GATEWAY")}/services'
    name = "authentication"
    try:
        res = post(
            url=base_url,
            data={"name": name, "url": getenv("AUTHENTICATION_URL")},
        )

        if res.status_code == 201:
            post(
                url=f"{base_url}/{name}/routes",
                data={"name": "signin", "paths[]": "/signin"},
            )

            print("Created gateway connection!")

            return
        elif res.status_code == 409:
            print("Gateway connection already created!")
            
            return
        else:
            print("Could not create gateway connection!")

    except:
        print("Gateway is not available!")

    sleep(0.2)

    if attempts <= MAX_RETRIES:
        establish_gateway_connection(attempts=attempts + 1)

@app.route("/signin", methods=["POST"])
def signin():
    client_id = request.args.get("client_id")
    code = request.args.get("code")
    return authenticate(client_id, code)


if __name__ == "__main__":
    establish_gateway_connection()

    app.run(debug=getenv("DEVELOPMENT"), host="0.0.0.0", port=getenv("PORT"))
