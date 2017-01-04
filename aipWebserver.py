from celery import Celery
from flask import Flask, request, json, jsonify

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/')
def hello_world():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            print(isinstance(data, dict))
            print(data)
            return jsonify(data)
        else:
            data = request.form
            print(data)
    return '<h1>Hello World!</h1>'


@celery.task
def my_background_task(arg1, arg2):
    # some long running task here
    return arg1 + arg2


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4999, debug=True)
