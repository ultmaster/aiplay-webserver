from celery import Celery
from flask import Flask, request, json, jsonify
from config import *
from core.handler import Handler
from core.tester import Tester
from local_config import *


def verify_token(data):
    if data.get('token') is None:
        return False
    token = data.get('token')
    try:
        with open(TOKEN_FILE_PATH, 'r') as f:
            self_token = f.read().strip()
    except OSError:
        self_token = ''
    if self_token != token:
        return False
    return True


@app.route('/judge', methods=['POST'])
def server_judge():
    result = {'status': 'reject'}
    if request.is_json:
        try:
            data = request.get_json()
            if verify_token(data):
                result.update(Handler(data).run())
                result['status'] = 'received'
        except Exception as e:
            print(e)
    return jsonify(result)


@app.route('/test', methods=['POST'])
def server_test():
    result = {'status': 'reject'}
    if request.is_json:
        try:
            data = request.get_json()
            if verify_token(data):
                result.update(Tester(data).test())
                result['status'] = 'received'
        except Exception as e:
            print(e)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4999, debug=DEBUG)
