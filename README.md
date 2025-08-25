# 🖼️ Object Detector (YOLOv8 + Flask + Docker Compose)

An end‑to‑end **object detection web app** built with:
- **YOLOv8** (Ultralytics) for inference
- **Flask** for both the **AI API** and the **UI**
- **Docker Compose** to run both services together

The system has two services:
- **AI Service (`ai_service`)** — Flask REST API that performs object detection with YOLOv8
- **UI Service (`ui_service`)** — Flask web app to upload images and view results

Both services share a common folder: `shared/uploads`.

---

## 📂 Project Structure

```plaintext
Object-Detector/
│
├── ai_service/                # Object detection backend (YOLOv8 + Flask API)
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── yolov8.pt              # YOLOv8 weights (optional - will download yolov8n if missing)
│
├── ui_service/                # Frontend (Flask UI)
│   ├── templates/
│   │   └── index.html
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── shared/                    # Shared folder between services
│   └── uploads/               # Uploaded & processed images
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 Run with Docker (recommended)

```bash
docker compose up --build
```

- Builds images for both **ai_service** and **ui_service**
- Starts both services and mounts `./shared/uploads:/app/../shared/uploads`

Access the UI at: **http://localhost:5050**

---

## 🧑‍💻 Run Locally (without Docker)

> Requires **Python 3.10+** and **pip**. A virtualenv is recommended but optional.

### 1) Start the AI Service
```bash
cd ai_service
pip install -r requirements.txt
python3 app.py
```
This starts the YOLOv8 API on **http://127.0.0.1:8000**.

### 2) Start the UI Service (in a second terminal)
```bash
cd ui_service
pip install -r requirements.txt
python3 app.py
```
Now open **http://127.0.0.1:5050** in your browser.

### 3) Use the App
- Upload an image from the UI
- Click **Upload & Detect**
- See the detected objects (bounding boxes + labels) and the JSON result
- Processed image is saved as `boxed_<filename>` inside `shared/uploads`

> Both apps write/read from `../shared/uploads` relative to their working directories. The folders are created automatically if missing.

---

## 📦 API (Direct AI Service)

### Detect objects
```bash
curl -X POST http://127.0.0.1:8000/detect   -F "file=@image\ copy.png"
```

### Example JSON response
```json
{
  "detections": [
    { "label": "person", "box": [50, 80, 200, 300], "confidence": 0.92 }
  ],
  "image_url": "/uploads/boxed_image copy.png"
}
```

### Fetch processed image
The `image_url` is a relative path served by the AI service:
```
GET http://127.0.0.1:8000/uploads/boxed_image%20copy.png
```

---

## ⚙️ Environment Variables

| Variable          | Default                              | Used By     | Description                                  |
|-------------------|--------------------------------------|-------------|----------------------------------------------|
| `AI_SERVICE_URL`  | `http://ai_service:8000/detect`      | UI Service  | AI API endpoint (Docker). For local dev, UI defaults to `http://127.0.0.1:8000/detect`. |
| `PYTHONUNBUFFERED`| `1`                                  | Both        | Ensures logs are flushed to console in real-time. |

---

## 📝 Notes & Tips

- If `ai_service/yolov8.pt` is **not present**, the AI service will download a small model (`yolov8n.pt`) and save it as `yolov8.pt` on first run.
- The shared folder is **`shared/uploads`**. In Docker it is bind-mounted into both services at `/app/../shared/uploads`.
- If ports are busy, change them in the code or Docker Compose (`8000` for AI, `5050` for UI).

### Common Commands
```bash
# Rebuild & start (Docker)
docker compose up --build

# Stop services (Docker)
docker compose down

# Stop and remove volumes (Docker)
docker compose down -v
```

---

## ✅ Example Workflow

1. Start both services (Docker or local).
2. Open **http://localhost:5050**.
3. Upload an image.
4. The UI saves it to `shared/uploads` and calls the AI API.
5. The AI detects objects and writes `boxed_<filename>` back to `shared/uploads`.
6. The UI shows the processed image and the detection JSON.



---

## 📚 References

- [Docker Documentation](https://docs.docker.com/) – Compose, volumes, networking   
- [YOLOv8 Docs](https://docs.ultralytics.com/) – Model loading, inference, result parsing  
- **ChatGPT (OpenAI)** – Helped in improving the UI experience and making the README more structured and readable.  

---
