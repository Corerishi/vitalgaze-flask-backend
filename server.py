from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allow all origins and methods, including OPTIONS preflight
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.before_request
def handle_preflight():
    """Handles CORS preflight requests automatically."""
    if request.method == "OPTIONS":
        response = jsonify({"message": "CORS preflight success"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response, 200

@app.route('/')
def home():
    return "Flask API for Face Analysis"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        image_data = data.get("image")
        if not image_data:
            return jsonify({"error": "No image provided"}), 400

        return jsonify({"message": "Image received and processed!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)
