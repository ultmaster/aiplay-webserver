from celery import Celery
from flask import Flask, request, json, jsonify
from config import *
from core.handler import Handler


@app.route('/judge', methods=['POST'])
def server_judge():
    result = {'status': 'reject'}
    if request.is_json:
        result['status'] = 'received'
        result.update(Handler(request.get_json()).run())
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4999, debug=True)
