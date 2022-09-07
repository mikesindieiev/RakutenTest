from flask import Flask, jsonify, request
import os
import shutil

app = Flask(__name__)


@app.route('/', methods=['GET'])
def fetch_response():
    return jsonify({"message": 'Hello from get'})


@app.route('/', methods=['POST'])
def run_scanner():
    # Get json from http body. Todo verify that we receiving body with application/json header, either return error
    data = request.get_json()

    source_code_url = None
    lang = None
    scanner_name = None

    # Todo add error handling, one field is missing etc
    if data:
        if 'source_code_url' in data:
            source_code_url = data['source_code_url']
        if 'lang' in data:
            lang = data['lang']
        if 'scanner_name' in data:
            scanner_name = data['scanner_name']

    # Get dir name from source_code_url and get latest code from repo.
    # Todo: handle cases when latest element ends with dot
    code_dir = source_code_url.split('/')[-1]
    shutil.rmtree(code_dir, ignore_errors=True)

    # Clone the repo
    os.system('git clone {0}'.format(source_code_url))
    return jsonify({"message": "success"})


if __name__ == '__main__':
    app.run()
