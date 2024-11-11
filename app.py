from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import signal
import sys


def handle_termination_signal(signum, frame):
    print("Application is terminating...")
    subprocess.run(["python", "delChaps.py"])
    sys.exit(0)


app = Flask(__name__)
CORS(app)

signal.signal(signal.SIGINT, handle_termination_signal)
signal.signal(signal.SIGTERM, handle_termination_signal)


@app.route('/outputing', methods=['POST'])
def outputing():
    data = request.json
    print(data)

    input_text = data.get('input')
    if not input_text:
        return jsonify({'error': "Null input"}), 500

    comment = data.get('comment')

    chap = "Chapter " + input_text + ".txt"

    try:
        file_path = chap

        if os.path.exists(file_path) and not comment:
            pass
        else:
            result = subprocess.run(
                ['python', 'shadowc.py', input_text, comment],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            print(result.stderr)

        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        return jsonify({'content': file_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
