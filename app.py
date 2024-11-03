from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os


app = Flask(__name__)
CORS(app)

@app.route('/outputing', methods=['POST'])
def outputing():
    data = request.json
    input_text = data.get('input')
    chap = "Chapter " + str(input_text) + ".txt"

    try:
        file_path = chap

        if os.path.exists(file_path):
            pass
        else:
            result = subprocess.run(
                ['python', 'shadowc.py', input_text],
                capture_output=True,
                text=True
            )


        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        return jsonify({'content': file_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
