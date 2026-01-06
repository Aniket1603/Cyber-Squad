from flask import Flask, render_template, request, jsonify
from model import forensic_audit_web

app = Flask(__name__)

# Route to serve your HTML page
@app.route('/')
def index():
    # Make sure your HTML file is named 'index.html' and inside a 'templates' folder
    return render_template('index.html')

# Route to handle the AJAX 'Fetch' request from your script
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image_file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['image_file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Call the model logic
    report = forensic_audit_web(file)
    
    # Send the data back to your JavaScript as JSON
    return jsonify(report)

if __name__ == '__main__':
    # Run the server on http://127.0.0.1:5000
    app.run(debug=True)