from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "OK",
        "service": "api-service",
        "timestamp": time.time()
    }), 200

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify({
        "records": [
            {"id": 101, "item": "Widget A", "price": 49.99},
            {"id": 102, "item": "Widget B", "price": 89.99}
        ],
        "count": 2
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
