from celery import Celery
from flask import Flask, request, json, jsonify
from config import *
from core.handle import Handler


@app.route('/', methods=['POST'])
def hello_world():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            # do something
            return jsonify({'status': 'accept'})
    return jsonify({'status': 'reject'})

@celery.task
def my_background_task(arg1, arg2):
    # some long running task here
    return arg1 + arg2


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4999, debug=True)
