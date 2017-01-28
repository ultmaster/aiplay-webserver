import uuid
import zipfile
import sys
from flask import Flask, request, jsonify
from config import *
from core.handler import Handler
from core.tester import Tester


def verify_token(data):
    try:
        try:
            self_token = open(TOKEN_FILE_PATH, 'r').read().strip()
        except OSError:
            self_token = ''
        if data.get('username') == 'token' and data.get('password') == self_token:
            return True
        return False
    except KeyError:
        return False


@app.route('/upload/<tag>/<id>', methods=['POST'])
def server_upload(tag, id):
    result = {'status': 'reject'}
    try:
        if int(id) < 0:
            raise ValueError
        if verify_token(request.authorization):
            if tag == 'pretest':
                target_dir = os.path.join(PRETEST_DIR, id)
            elif tag == 'data':
                target_dir = os.path.join(DATA_DIR, id)
            else:
                raise ValueError
            source_path = os.path.join(TMP_DIR, str(uuid.uuid1()) + '.zip')
            with open(source_path, 'wb') as f:
                f.write(request.data)
            source_zip = zipfile.ZipFile(source_path)
            source_zip.extractall(target_dir)
            source_zip.close()
            result['status'] = 'received'
            os.remove(source_path)
    except Exception as e:
        print(e)
    return jsonify(result)


@app.route('/judge', methods=['POST'])
def server_judge():
    result = {'status': 'reject'}
    if request.is_json:
        try:
            if verify_token(request.authorization):
                result.update(Handler(request.get_json()).run())
                result['status'] = 'received'
        except Exception as e:
            print(e)
    return jsonify(result)


@app.route('/test', methods=['POST'])
def server_test():
    result = {'status': 'reject'}
    if request.is_json:
        try:
            if verify_token(request.authorization):
                result.update(Tester(request.get_json()).test())
                result['status'] = 'received'
        except Exception as e:
            print(e)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999, debug=False)
