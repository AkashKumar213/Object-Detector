# Object Detector

This project provides a web-based object detection system consisting of two services:

- **ai_service**: A Flask API using YOLO (Ultralytics) to detect objects in uploaded images.
- **ui_service**: A Flask web interface that allows users to upload images, sends them to the AI service, and displays the detection results on the same page.

---

## Project Structure

.
├── ai_service
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
├── ui_service
│ ├── app.py
│ ├── requirements.txt
│ ├── templates
│ │ └── index.html
│ └── Dockerfile



---

## Prerequisites

- Python 3.9+ (for local runs)
- Docker and Docker Compose (for containerized runs)

---

## Running Locally

### 1. Start the AI Service



cd ai_service
pip install -r requirements.txt
python app.py



- This starts the AI service on `http://127.0.0.1:8000`.
- The YOLO model will download automatically on first run if not present.

### 2. Start the UI Service

Open a new terminal:

cd ui_service
pip install -r requirements.txt
python app.py



- This starts the UI service on `http://127.0.0.1:5050`.
- The UI expects the AI service at `http://127.0.0.1:8000/detect`.
- Shared image upload folder is referenced locally as `../shared/uploads` relative to each service.

---

## Running with Docker Compose

From the project root where `docker-compose.yml` is located, run:

docker-compose up --build

- Builds and runs AI and UI services in containers.
- Mounts a shared Docker volume `output_data` at `/app/output` in both containers for sharing images.
- AI service is accessible at `http://localhost:8000`.
- UI service is accessible at `http://localhost:5050`.
- UI communicates with AI internally using `http://ai_service:8000/detect`.

---

## Configuration Summary

| Setting                | Local Run Value                 | Docker Run Value                 |
|------------------------|--------------------------------|---------------------------------|
| AI service URL         | http://127.0.0.1:8000/detect   | http://ai_service:8000/detect   |
| Uploads folder path    | ../shared/uploads (relative)    | /app/output (shared volume)     |
| Ports exposed          | AI: 8000, UI: 5050             | Mapped 8000 and 5050            |

---

## Usage

- Open `http://localhost:5050` in your browser.
- Upload an image through the form.
- Wait for processing; results will show below the upload form.
- View the original image, processed image with bounding boxes, and detailed JSON of detections.

---

## Notes

- The UI and AI services share the uploads folder to allow retrieval of images.
- The app is designed so only `index.html` is needed; all results display dynamically on the same page.
- Model downloading is handled automatically by the AI service.
- Adjust environment variables or ports if running in different environments.

---

## Troubleshooting

- If images or detection results fail to show, verify shared folder paths and Docker volume mounts.
- Connection errors typically arise from incorrect AI service URLs—check environment variables.
- For slow first runs, the YOLO model download may take some time.
- Ensure ports 8000 and 5050 are free before running services.

---

## License

This project is licensed under the MIT License.

---

This README provides all necessary instructions to develop, test, and run the combined object detection system locally or inside Docker containers with a smooth user experience on a single web page.
