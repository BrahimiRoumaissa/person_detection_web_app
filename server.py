from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import threading
import time
import ssl
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize YOLO model
model = YOLO('yolov8n.pt').cpu()
model.conf = 0.5
model.iou = 0.45

# Global variables
person_count = 0
last_frame = None
lock = threading.Lock()

def process_frame(frame_data):
    global person_count, last_frame
    
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(frame_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Run YOLO detection
        results = model(frame, stream=True)
        
        # Process detections
        person_count = 0
        for r in results:
            for box in r.boxes:
                if int(box.cls[0]) == 0:  # Person class
                    conf = float(box.conf[0])
                    if conf > 0.5:
                        person_count += 1
                        # Draw rectangle around the person
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f'Person: {conf:.2f}', (x1, y1-10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Update last frame
        with lock:
            last_frame = frame
            
    except Exception as e:
        print(f"Error processing frame: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def handle_frame():
    try:
        data = request.json
        frame_data = data['image']
        
        # Process frame in a separate thread
        threading.Thread(target=process_frame, args=(frame_data,)).start()
        
        # Return the processed frame if available
        with lock:
            if last_frame is not None:
                _, buffer = cv2.imencode('.jpg', last_frame)
                frame_bytes = base64.b64encode(buffer).decode('utf-8')
                return jsonify({
                    'status': 'success',
                    'frame': frame_bytes,
                    'count': person_count
                })
            return jsonify({'status': 'processing'})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/person_count', methods=['GET'])
def get_person_count():
    return str(person_count)

if __name__ == '__main__':
    try:
        # Verify SSL certificate files exist
        if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
            raise FileNotFoundError("SSL certificate files not found. Please generate them first.")
        
        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        
        print("Starting server with HTTPS...")
        print("Access the application at: https://<your-ip>:5000")
        print("Note: You may need to accept the security warning in your browser")
        
        # Run the app with HTTPS
        app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=context)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Make sure you have generated the SSL certificates and they are in the correct location.") 