

# Real-time Person Detection System

A real-time person detection system that uses your phone's camera to capture video, processes it on a PC using YOLOv8, and displays the results back on your phone. This project demonstrates how to create a distributed computer vision system using web technologies.

## Features

- Real-time person detection using YOLOv8
- Mobile-friendly web interface
- Secure HTTPS communication
- Cross-platform compatibility
- Live video streaming with detection boxes
- Person count display
- Start/Stop detection control

## Prerequisites

- Python 3.7 or higher
- Webcam or phone camera
- Local network connection between phone and PC
- Modern web browser (Chrome, Firefox, Safari, etc.)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BrahimiRoumaissa/person-detection.git
cd person-detection
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Generate SSL certificates for HTTPS:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

## Usage

1. Start the server on your PC:
```bash
python server.py
```

2. Find your PC's IP address:
```bash
ip addr
```

3. On your phone:
   - Open your web browser
   - Navigate to: `https://<your-pc-ip>:5000`
   - Accept the security warning (self-signed certificate)
   - Allow camera access when prompted
   - Click "Start Detection" to begin

## Project Structure

```
person-detection/
├── server.py           # Flask server with YOLO processing
├── templates/
│   └── index.html     # Web interface
├── requirements.txt   # Python dependencies
├── cert.pem          # SSL certificate
├── key.pem           # SSL private key
└── README.md         # This file
```

## How It Works

1. The web interface captures video from your phone's camera
2. Each frame is sent to the PC server via HTTPS
3. The server processes the frame using YOLOv8
4. Detected persons are marked with bounding boxes
5. The processed frame and person count are sent back to the phone
6. The web interface displays the results in real-time

## Security Notes

- The application uses HTTPS with a self-signed certificate for development
- Camera access requires HTTPS (secure context)
- All communication between phone and PC is encrypted
- The system runs on your local network only

## Performance Considerations

- Processing is done on the PC to leverage its computing power
- Video quality and frame rate can be adjusted based on network conditions
- The system uses YOLOv8n (nano) model for better performance
- Confidence threshold is set to 0.5 to balance accuracy and speed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/)
