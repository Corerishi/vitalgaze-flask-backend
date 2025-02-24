import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS for all domains, including localhost
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/')
def home():
    return jsonify({"message": "Flask API is working!"})

@app.route('/analyze', methods=['OPTIONS'])
def handle_preflight():
    """Handles CORS preflight requests before the actual request."""
    response = jsonify({"message": "CORS preflight success"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response, 200

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        image_data = data.get("image")
        if not image_data:
            return jsonify({"error": "No image provided"}), 400

        response = jsonify({"message": "Image received and processed!"})
        response.headers.add("Access-Control-Allow-Origin", "*")  # Fix CORS
        return response

    except Exception as e:
        response = jsonify({"error": str(e)})
        response.headers.add("Access-Control-Allow-Origin", "*")  # Fix CORS
        return response, 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port, debug=True)
