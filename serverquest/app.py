from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask import abort

from . controller import create_user
from . controller import get_jwt

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


@app.route("/users", methods=["POST"])
def post_user ():
    user_data = request.get_json()

    _assert("email" in user_data, 400, "no email in user's data")
    _assert("password" in user_data, 400, "no password in user's data")
    _assert("name" in user_data, 400, "no name in user's data")

    try:
        create_user(user_data)
    except AssertionError as e:
        _abort(str(e), 400)

    res = {
        'status_code': '201 CREATED',
        'message': 'User created with success.',
        'data': { 'user_data': user_data }
    }
    return jsonify(res), 201


@app.route('/auth/login', methods=['POST'])
def login():
    user_data = request.get_json()

    _assert('email' in user_data, 400, "No email in user's data.")
    _assert("password" in user_data, 400, "No password in user's data.")

    try:
        jwt = get_jwt(user_data)
    except AssertionError as e:
        _abort(str(e), 401)
    
    res = {
        'status_code': '200 OK',
        'message': 'Login authorized.',
        'data': { 'jwt': jwt }
    }

    return jsonify(res), 200


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

