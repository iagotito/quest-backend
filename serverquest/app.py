from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask import abort

from . controller import create_user

app = Flask(__name__)


def _assert(condition, status_code, message):
    if condition: return
    data = {
        "message": message,
        "status_code": status_code
    }
    response = make_response(jsonify(data), status_code)
    abort(response)


def _abort(status_code, message, data=None):
    _assert(False, message, status_code)


@app.route("/status", methods=["GET"])
def get_status ():
    return jsonify({"status": "running"}), 200


@app.route("/user", methods=["POST"])
def post_user ():
    req = request.get_json()

    _assert("email" in req, 400, "no email in user's info")
    _assert("password" in req, 400, "no password in user's info")
    _assert("name" in req, 400, "no name in user's info")

    try:
        new_user = create_user(req)
    except AssertionError as e:
        _abort(str(e), 400)

    return new_user, 201


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

