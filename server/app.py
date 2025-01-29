from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/historical')
def historical():
    # Your data processing here
    return jsonify(your_data)

if __name__ == '__main__':
    app.run(port=5000) 