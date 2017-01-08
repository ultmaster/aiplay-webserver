from celery import Celery
from flask import Flask, request, json, jsonify
from config import *
from core.handler import Handler


@app.route('/', methods=['POST'])
def hello_world():
    if request.is_json:
        data = request.get_json()
        print(data)
        Handler(data).run()
        return jsonify({'status': 'accept'})
    return jsonify({'status': 'reject'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4999, debug=True)
