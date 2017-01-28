import uuid
import zipfile
from flask import Flask, request, jsonify
from config import *
from core.handler import Handler
from core.tester import Tester
from local_config import *


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


@app.route('/upload', methods=['POST'])
def server_upload():
    result = {'status': 'reject'}
    try:
        if verify_token(request.authorization):
            target_dir = JUDGE_BASE_DIR
            source_path = os.path.join(TMP_DIR, str(uuid.uuid1()) + '.zip')
            with open(source_path, 'wb') as f:
                f.write(request.data)
            source_zip = zipfile.ZipFile(source_path)
            file_list = source_zip.namelist()
            for name in file_list:
                f_handle = open(os.path.join(target_dir, name), "wb")
                f_handle.write(source_zip.read(name))
                f_handle.close()
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
    app.run(host='127.0.0.1', port=4999, debug=DEBUG)
