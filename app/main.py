# app/main.py

import os
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
from utils import run_openmvg_pipeline
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'app/static'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
CORS(app)  # 允许所有跨域请求

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    files = request.files.getlist('images')
    if not files:
        return jsonify({'error': 'No files uploaded'}), 400

    session_id = str(uuid.uuid4())
    session_path = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(session_path, exist_ok=True)

    for file in files:
        print("Saving file:", file.filename)
        file.save(os.path.join(session_path, file.filename))

    try:
        output_model_path = run_openmvg_pipeline(session_path, session_id)
    except Exception as e:
        print("Pipeline failed:", e)
        return jsonify({'error': '3D model generation failed', 'details': str(e)}), 500

    if not output_model_path:
        return jsonify({'error': '3D model generation failed'}), 500

    return jsonify({
        'message': 'Model generated successfully',
        'model_url': f'/download/{session_id}/openMVS/scene_mesh.ply'
    })

@app.route('/download/<session_id>/<subfolder>/<filename>', methods=['GET'])
def download_model(session_id, subfolder, filename):
    session_path = os.path.join(app.config['RESULT_FOLDER'], session_id, subfolder)
    file_path = os.path.join(session_path, filename)

    if not os.path.isfile(file_path):
        return jsonify({'error': 'File not found'}), 404

    return send_from_directory(session_path, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# 或更简单的全局允许
CORS(app)