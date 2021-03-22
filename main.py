from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv

from lib.github import authenticate

load_dotenv()


app = Flask(__name__)
CORS(app)


@app.route("/signin", methods=['POST'])
def signin():
    client_id = request.args.get('client_id')
    code = request.args.get('code')
    return authenticate(client_id, code)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=getenv("PORT"))
