from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
from src.analyzer import analyze_files
import uuid

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return redirect(url_for('index'))
    files = request.files.getlist('files')
    saved = []
    for f in files:
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            uid = str(uuid.uuid4())[:8]
            out_name = f"{uid}__{filename}"
            path = os.path.join(app.config['UPLOAD_FOLDER'], out_name)
            f.save(path)
            saved.append(out_name)
    return redirect(url_for('index'))

@app.route('/analyze', methods=['GET'])
def analyze():
    files = request.args.get('files')
    last_n = int(request.args.get('last_n', 100))
    if not files:
        return jsonify({'error': 'no files specified'}), 400
    file_list = files.split(',')
    file_paths = [os.path.join(app.config['UPLOAD_FOLDER'], f) for f in file_list]
    result = analyze_files(file_paths, last_n=last_n)
    return jsonify(result)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


app.run(host='0.0.0.0', port=5000)
