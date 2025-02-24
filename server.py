from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from main import FacialHealthAnalyzer

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins


app = Flask(__name__)
CORS(app)  # Allows frontend to send requests

analyzer = FacialHealthAnalyzer()  # Load your analysis model

@app.route('/')
def home():
    return "Flask API for Face Analysis"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        image_data = data['image']
        decoded_data = base64.b64decode(image_data)
        np_arr = np.frombuffer(decoded_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        analyzed_frame, results = analyzer.analyze_face(frame)
        if results is None:
            return jsonify({"error": "No face detected"}), 400

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's assigned port
    app.run(host='0.0.0.0', port=port, debug=True)

