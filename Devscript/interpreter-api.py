from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from interpreter.interpretertry import run_script

app = Flask(__name__)
CORS(app)

@app.route('/run_script', methods=['POST'])
def execute_script():
    try:
        data = request.json
        script = data.get('script')
        result = run_script(script)
        return jsonify({
            'status': 'success',
            'data': result,
            'metadata': {
                'script_length': len(script),
                'timestamp': time.time()
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
