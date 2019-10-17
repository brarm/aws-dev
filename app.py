#!/usr/bin/env python

from flask import Flask
from flask import url_for
from flask import request
from flask import Response
from flask import jsonify
from flask import render_template
from flask import g
from flask import send_from_directory

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

@app.route('/kba-questions', methods=['POST', 'GET'])
def kba_questions():
    if request.method == 'GET':
        return render_template('kba-not-found.html')
    else:
        raw_data = request.form
        kba_string = (raw_data.to_dict())['payload']
        kba_questions = json.loads(kba_string)['kba_questions']

        return render_template('kba-questions.html', kba_questions=kba_questions)

@app.route('/kba-success', methods=['POST'])
def kba_success():
    raw_data = request.form
    # handle risk score parsing here
    return render_template('kba-success.html')

@app.route('/kba-failed', methods=['POST'])
def kba_failed():
    raw_data = request.form
    print(raw_data)
    message = (raw_data.to_dict())['payload']
    print(message)
    message_lines = message.split(';;')
    print(message_lines)
    return render_template('kba-failed.html', message_lines=message_lines)

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    
    return render_template('not-found.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico')

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
    app.run(host='0.0.0.0', port=80, debug=False, threaded=True)
