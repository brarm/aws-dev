from flask import Flask
from flask import url_for
from flask import request
from flask import Response
from flask import jsonify
from flask import render_template
from flask import g

import os
import json

from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    if not request.script_root:
        # this assumes that the 'index' view function handles the path '/'
        request.script_root = url_for('index', _external=True)
    return render_template('index.html')

@app.route('/kba-quiz', methods=['POST'])
def kba_quiz():
    raw_data = request.form
    kba_string = (raw_data.to_dict())['payload']
    kba_questions = json.loads(kba_string)['kba_questions']

    print(json.dumps(kba_questions, indent=2))

    return render_template('kba-quiz.html', kba_questions=kba_questions)
    return jsonify({'message': 'kba-quiz'})

@app.route('/hello', methods = ['GET'])
def api_hello():
    data = {
        'hello' : 'world',
        'number'    : 3
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost'

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    
    return resp

@app.route('/echo', methods= ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    data = {
        'message' : 'ECHO: ' + request.method
    }

    resp = jsonify(data)
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

def check_auth(username, password):
    return username =='admin' and password == 'secret'

def authenticate(user=None):
    
    message = {
        'message'   : 'Authentication failed',
        'user'      :  user
        }
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()
        elif not check_auth(auth.username, auth.password):
            return authenticate(auth.username)
        return f(*args, **kwargs)

    return decorated


@app.route('/secrets', methods=['GET'])
@requires_auth
def secrets():
    message = {'message' : 'Authentication presented succesfully'}
    return jsonify(message)

if __name__ == '__main__':
    app.run()
