from Modules import Writer
from flask import Flask, Response, request
from Auth import auth, add_user_token
import os
import json


app = Flask(__name__)


@app.route('/ok', methods=['POST'])
def ok():
    return Response(status=200, response="OK")

@app.route('/write', methods=['POST'])
@auth.login_required
def write():
    body = request.get_json()
    wr = Writer(body['file'], body['mode'])
    wr.write(body['text'])
    return Response(status=200, response="Alegria")

@app.route('/')
@auth.login_required
def index():
    return f"Hello, {auth.current_user()}!"

@app.route('/create_user', methods=['POST'])
@auth.login_required
def create_user():
    body = request.get_json()
    return Response(status=200, response=json.dumps(add_user_token(body['user_name'])))

if __name__ == '__main__':
    for file in os.listdir():
        if '.txt' in file:
            os.remove(file)
    app.run()