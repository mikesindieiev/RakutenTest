import json
import os
import shutil
import logging
from string import Template

from flask import Flask, jsonify, request

app = Flask(__name__)

report_file = './report.json'
logging.basicConfig(format='%(asctime)s-%(levelname)s-%(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')


@app.route('/', methods=['GET'])
def fetch_response():
    # Return the scan result to the user. If it is not present - return 404
    try:
        with open(report_file, 'r') as f:
            report_json = json.load(f)
        app.logger.info("Sending report")
        app.logger.debug("Sent data: {0}".format(report_json))
        return report_json
    except Exception as e:
        app.logger.error("Error with opening the file")
        app.logger.debug("Exception: {0}".format(e))
        resp_json = {"message": "Report does not exist"}
        app.logger.debug("Sent data: {0}".format(resp_json))
        return jsonify(resp_json), 404


@app.route('/', methods=['POST'])
def run_scanner():
    # Get json from http body.
    # If received not JSON or application/json header is missing, returns code 400
    data = request.get_json()
    app.logger.debug("Received data from request: {0}".format(data))

    source_code_url = None
    lang = None
    scanner_name = None

    # Parse the input data and verify that all fields are present. If no - return the error to user
    error_message_tmlpt = Template("Error. $missing_field field is missed in request JSON")
    fields = ['source_code_url', 'lang', 'scanner_name']
    if data:
        for one_field in fields:
            if one_field in data and one_field == 'source_code_url':
                source_code_url = data['source_code_url']
            elif one_field in data and one_field == 'lang':
                lang = data['lang']
            elif one_field in data and one_field == 'scanner_name':
                scanner_name = data['scanner_name']
            else:
                resp_message = {"message": error_message_tmlpt.substitute(missing_field=one_field)}
                app.logger.debug("Sent message: {0}".format(resp_message))
                # is wrong data from client are server errors?
                app.logger.warning(error_message_tmlpt.substitute(missing_field=one_field))
                return jsonify(resp_message), 400
    else:
        resp_message = {"message": "No data received"}
        app.logger.warning("Received empty request")
        app.logger.debug("Sent message: {0}".format(resp_message))
        return jsonify(resp_message), 400

    # Get dir name from source_code_url and get latest code from repo.
    code_dir = source_code_url.split('/')[-1]
    shutil.rmtree(code_dir, ignore_errors=True)

    # Execute scan.
    os.system('git clone {0}'.format(source_code_url))
    app.logger.debug("Cloned the repo")

    os.system('/usr/src/app/bin/brakeman ./{0} -o {1}'.format(code_dir, report_file))
    app.logger.debug("Run scan")

    success_msg = {"message": "success"}
    app.logger.debug("Sent message: {0}".format(success_msg))
    app.logger.info("Report created")
    return jsonify(success_msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
