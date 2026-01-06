from flask import Flask, render_template, request, jsonify
from model import forensic_audit_web

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image_file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['image_file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    report = forensic_audit_web(file)
    
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True)