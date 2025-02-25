import os
import mimetypes
from flask import Flask, request, jsonify
from flask_cors import CORS
import main  # Import main.py where your analysis happens

app = Flask(__name__)

# Allow CORS for all domains, including localhost
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']

        # Validate file type
        if not allowed_file(image_file.filename):
            return jsonify({"error": "Invalid file format. Use PNG, JPG, or JPEG."}), 400

        # Ensure MIME type is correct
        mime_type, _ = mimetypes.guess_type(image_file.filename)
        if not mime_type or not mime_type.startswith("image"):
            return jsonify({"error": "Invalid file type."}), 400

        # Process image using main.py function
        analysis_result = main.process_image(image_file)

        response = jsonify(analysis_result)
        response.headers.add("Access-Control-Allow-Origin", "*")  # Fix CORS
        return response

    except Exception as e:
        response = jsonify({"error": str(e)})
        response.headers.add("Access-Control-Allow-Origin", "*")  # Fix CORS
        return response, 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port if deploying
    app.run(host="0.0.0.0", port=port, debug=True)
