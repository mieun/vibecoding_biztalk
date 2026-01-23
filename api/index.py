from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from services import convert_text
import os

# Set the static folder to the 'public' directory, which is one level up from 'api'
current_dir = os.path.dirname(os.path.abspath(__file__))
public_folder = os.path.join(current_dir, '..', 'public')

app = Flask(__name__, static_folder=public_folder, static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"})

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json()
    
    if not data or 'text' not in data or 'target' not in data:
        return jsonify({"error": "Missing 'text' or 'target' in request body"}), 400
        
    text = data['text']
    target = data['target']
    lang = data.get('lang', 'ko') # Default to Korean if not provided
    
    # Validation
    if len(text) > 500:
        return jsonify({"error": "Text exceeds 500 characters limit"}), 400
        
    try:
        result = convert_text(text, target, lang)
        return jsonify({"original": text, "converted": result, "target": target, "lang": lang})
    except Exception as e:
        # In production, log the error securely
        print(f"Error during conversion: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
