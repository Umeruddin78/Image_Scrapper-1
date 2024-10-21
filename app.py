from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import shutil
import requests
from backend import scrape_google_images

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/search', methods=['POST'])
def search_images():
    if request.method == 'POST':
        data = request.get_json()
        search_query = data.get('query')
        quantity = int(data.get('quantity', 10))  # Default to 10 if quantity is not provided
        image_urls = scrape_google_images(search_query, quantity)

        if image_urls:
            return jsonify({'status': 'success', 'image_urls': image_urls})
        else:
            return jsonify({'status': 'error', 'message': 'No or bad internet.'})
    else:
        return jsonify({'status': 'error', 'message': 'Unsupported method'})

@app.route('/download', methods=['POST'])
def download_images():
    if request.method == 'POST':
        data = request.get_json()
        search_query = data.get('query')
        image_urls = data.get('image_urls')

        temp_dir = f'temp_{search_query.replace(" ", "_")}'
        os.makedirs(temp_dir, exist_ok=True)

        for i, url in enumerate(image_urls):
            filename = f'image_{i+1}.jpg'
            image_path = os.path.join(temp_dir, filename)
            response = requests.get(url, stream=True)
            with open(image_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)

        zip_filename = f'{search_query}_images.zip'
        shutil.make_archive(temp_dir, 'zip', temp_dir)

        zip_file_path = f'{temp_dir}.zip'
        response = send_file(zip_file_path, as_attachment=True)

        shutil.rmtree(temp_dir)

        return response
    else:
        return jsonify({'status': 'error', 'message': 'Unsupported method'})

if __name__ == '__main__':
    app.run(debug=True, port=5005)
