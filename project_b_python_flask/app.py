from flask import Flask, jsonify, request
import time

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "UP",
        "timestamp": time.time(),
        "service": "Flask-Benchmark-Service"
    }), 200

@app.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Developer')
    return jsonify({
        "message": f"Hello, {name}!",
        "success": True
    }), 200

@app.route('/api/compute', methods=['POST'])
def compute():
    data = request.get_json() or {}
    number = data.get('number', 0)
    
    # Simple CPU-bound computation simulation
    result = sum(i * i for i in range(min(number, 100000)))
    
    return jsonify({
        "input": number,
        "result": result,
        "processed": True
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
