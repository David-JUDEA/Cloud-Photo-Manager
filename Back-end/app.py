from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import sqlite3
import os

app = Flask(__name__)
CORS(app)

endpoint = os.environ.get('AWS_ENDPOINT_URL', 'http://localhost:4566')

s3 = boto3.client(
    's3',
    endpoint_url=endpoint,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

BUCKET_NAME = "cloud-photo-bucket"

def init_db():
    conn = sqlite3.connect('DB.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, s3_url TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier envoyé"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400

    try:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    file_url = f"s3://{BUCKET_NAME}/{file.filename}"
    
    conn = sqlite3.connect('DB.db')
    c = conn.cursor()
    c.execute("INSERT INTO images (filename, s3_url) VALUES (?, ?)", (file.filename, file_url))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Image uploadée", "filename": file.filename, "url": file_url})

@app.route('/images', methods=['GET'])
def get_images():
    conn = sqlite3.connect('DB.db')
    c = conn.cursor()
    c.execute("SELECT filename, s3_url FROM images")
    rows = c.fetchall()
    conn.close()
    
    results = [{"filename": r[0], "url": r[1]} for r in rows]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
