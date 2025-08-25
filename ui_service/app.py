from flask import Flask, request, jsonify, render_template, send_from_directory
import requests
import os

app = Flask(__name__)
AI_SERVICE_URL=os.getenv("AI_SERVICE_URL", "http://127.0.0.1:8000/detect")

UPLOAD_FOLDER = "../shared/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    img_file = request.files['image']
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    upload_path = os.path.join(UPLOAD_FOLDER, img_file.filename)
    img_file.save(upload_path)

    # Send image to AI service
    with open(upload_path, 'rb') as f:
        files = {'file': (img_file.filename, f, img_file.content_type)}
        response = requests.post(AI_SERVICE_URL, files=files)

    if response.status_code != 200:
        return jsonify({"error": f"AI service error: {response.text}"}), 500

    result = response.json()
    
    output_img_path = result.get("image_url", "")  # Example: '/uploads/boxed_filename.jpg'
    detections = result.get("detections", [])

    return jsonify({
        "input_image": img_file.filename,
        "output_image": os.path.basename(output_img_path),
        "output_img_url": output_img_path,
        "detections": detections
    })



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
