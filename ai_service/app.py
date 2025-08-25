from flask import Flask, request, jsonify, send_from_directory
from ultralytics import YOLO
import os
import shutil
import cv2
import numpy as np

app = Flask(__name__)

# Paths
UPLOAD_FOLDER = '../shared/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MODEL_PATH = "yolov8.pt"
if not os.path.exists(MODEL_PATH):
    print(f"{MODEL_PATH} not found. Downloading...")
    model = YOLO("yolov8n.pt")
    shutil.move("yolov8n.pt", MODEL_PATH)
else:
    model = YOLO(MODEL_PATH)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/detect', methods=['POST'])
def detect_objects():
    if 'file' not in request.files:
        return jsonify({"error": "No file in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded image in uploads folder
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(img_path)

    # Perform detection with YOLO
    results = model(img_path)
    img = cv2.imread(img_path)

    detections = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()

        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = map(int, box)
            label = model.names[int(cls)]
            detections.append({
                "label": label,
                "box": [x1, y1, x2, y2],
                "confidence": float(conf)
            })
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(img, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
    # Save processed output image in uploads folder
    output_filename = f"boxed_{file.filename}"
    output_img_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    cv2.imwrite(output_img_path, img)

    # Return JSON with detection and URL to processed image
    return jsonify({
        "detections": detections,
        "image_url": f"/uploads/{output_filename}"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)
