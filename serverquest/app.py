from flask import Flask
from flask import request
from flask import jsonify
from flask import make_response
from flask import abort

from . controller import create_user
from . controller import get_jwt
from . controller import get_user_data
from . controller import create_tag
from . controller import get_user_tags
from . controller import create_todo
from . controller import get_user_todos
from . controller import update_todo_done

app = Flask(__name__)


def _make_response(message, status_code, data=None):
    res = {
        'message': message,
        'status_code': status_code
    }

    if data is not None:
        res['data'] = data
    
    return jsonify(res), status_code


def _assert(condition, status_code, message):
    if condition: return
    data = {
        "message": message,
        "status_code": status_code
    }
    response = make_response(jsonify(data), status_code)
    abort(response)


def _abort(status_code, message):
    _assert(False, message, status_code)


@app.route("/status", methods=["GET"])
def get_status ():
    return jsonify({"status": "running"}), 200


@app.route("/users", methods=["POST"])
def post_user ():
    user_data = request.get_json()

    _assert("email" in user_data, 400, "No email in user's data.")
    _assert("password" in user_data, 400, "No password in user's data.")
    _assert("name" in user_data, 400, "No name in user's data.")

    try:
        user_repr = create_user(user_data)
    except AssertionError as e:
        _abort(str(e), 400)

    data = { 'user_repr': user_repr }

    return _make_response('User created with success.', 201, data)


@app.route('/auth/login', methods=['POST'])
def login():
    user_data = request.get_json()

    _assert('email' in user_data, 400, "No email in user's data.")
    _assert("password" in user_data, 400, "No password in user's data.")

    try:
        jwt = get_jwt(user_data)
    except AssertionError as e:
        _abort(str(e), 401)
    
    data = { 'jwt': jwt }
    return _make_response('Loguin authorized.', 200, data)


@app.route('/auth/users', methods=['GET'])
def get_user():
    _assert('Authorization' in request.headers, 401, 'Missing Authorization header.')

    jwt = request.headers.get('Authorization')
    
    try:
        user_repr = get_user_data(jwt)
    except AssertionError as e:
        if str(e) == 'Signature expired.':
            _abort(str(e), 401)
        else:
            _abort(str(e), 400)
    

    data = { 'user_data': user_repr }

    return _make_response('User authorized.', 200, data)


@app.route('/auth/tags', methods=['POST'])
def post_tag():
    _assert('Authorization' in request.headers, 401, 'Missing Authorization header.')
    jwt = request.headers.get('Authorization')

    tag_data = request.get_json()
    _assert('tag_name' in tag_data, 400, "No name in tag's data")

    try:
        tag = create_tag(jwt, tag_data)
    except AssertionError as e:
        _abort(str(e), 400)
    
    data = { 'tag_repr': tag }
    
    return _make_response('Tag created.', 201, data)


@app.route('/auth/tags', methods=['GET'])
def get_tags():
    _assert('Authorization' in request.headers, 401, 'Missing Authorization header.')
    jwt = request.headers.get('Authorization')

    try:
        tags = get_user_tags(jwt)
    except AssertionError as e:
        _abort(str(e), 400)

    data = {
        'tags': tags,
        'num_tags': len(tags)
    }

    return _make_response(f'{len(tags)} tags returned.', 200, data)


@app.route('/auth/tag/<tag_name>/todos', methods=['POST'])
def post_todo(tag_name):
    _assert('Authorization' in request.headers, 401, 'Missing Authorization header.')
    jwt = request.headers.get('Authorization')

    _assert(tag_name, 400, 'Tag name cannot be empty string.')
    tag_name = tag_name.replace('-', ' ')

    todo_info = request.get_json()
    _assert('description' in todo_info, 400, "Missing 'description' field in todo_info.")

    try:
        todo = create_todo(jwt, tag_name, todo_info)
    except AssertionError as e:
        if str(e) == 'Signature expired.':
            _abort(str(e), 401)
        else:
            _abort(str(e), 400)

    data = {
        'todo': todo
    }
    
    return _make_response('Todo created', 201, data)
 

@app.route('/auth/tag/<tag_name>/todos', methods=['GET'])
def get_todos(tag_name):
    _assert('Authorization' in request.headers, 401, 'Missing Authorization header.')
    jwt = request.headers.get('Authorization')

    _assert(tag_name, 400, 'Tag name cannot be empty string.')
    tag_name = tag_name.replace('-', ' ')

    done = request.args.get('done')
    if done:
        if done.lower() == 'true': done = True
        elif done.lower() == 'false': done = False
        _assert(type(done) is bool, 400, 'Done must be boolean.')

    try:
        todos = get_user_todos(jwt, tag_name, done)
    except AssertionError as e:
        if str(e) == 'Signature expired.':
            _abort(str(e), 401)
        else:
            _abort(str(e), 400)

    data = {
        'todos': todos,
        'num_todos': len(todos)
    }
    if done is not None:
        data['query'] = f'done={done}'
    return _make_response(f'{len(todos)} todo returned.', 200, data)


@app.route('/auth/tag/<tag_name>/todo/<todo_id>', methods=['PATCH'])
def patch_todo(tag_name, todo_id):
    _assert('Authorization' in request.headers, 401, 'Missing Authorization header.')
    jwt = request.headers.get('Authorization')

    _assert(tag_name, 400, 'Tag name cannot be empty string.')
    tag_name = tag_name.replace('-', ' ')

    _assert((type(todo_id) is int or todo_id.isdigit()) and int(todo_id) >= 1, 400, 'Todo ID must be an integer greater than zero.')

    mark_as = request.args.get('mark_as')
    _assert(mark_as, 400, 'Missing mark_as argument.')
    if mark_as.lower() == 'true': mark_as = True
    elif mark_as.lower() == 'talse': mark_as = False
    _assert(type(mark_as) is bool, 400, 'mark_as must be boolean.')

    try:
        patched_todo = update_todo_done(jwt, tag_name, todo_id, mark_as)
    except AssertionError as e:
        if str(e) == 'Signature expired.':
            _abort(str(e), 401)
        else:
            _abort(str(e), 400)

    data = {
        'patched_todo': patched_todo
    }
    return _make_response(f'Todo {todo_id} done marked as {mark_as}', 200, data)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
