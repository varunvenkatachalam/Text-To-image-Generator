from flask import Flask, request, jsonify, render_template
import requests
import io
from PIL import Image
import base64

app = Flask(__name__)

# Configure your Hugging Face API key and endpoint
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"API request failed with status code {response.status_code}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        text = data['text']
        image_bytes = query({"inputs": text})

        # Convert the image bytes to a base64 string to send it in the response
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        image_url = f"data:image/png;base64,{image_base64}"

        return jsonify({'image_url': image_url})
    
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
