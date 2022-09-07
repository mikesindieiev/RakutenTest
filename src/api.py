from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def fetch_response():
    return jsonify({"message": 'Hello from get'})


@app.route('/', methods=['POST'])
def run_scanner():
    return jsonify({"message": 'Hello from post'})


if __name__ == '__main__':
    app.run()
