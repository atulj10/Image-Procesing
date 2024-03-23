from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Check if the 'uploads' directory exists, if not, create it
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to process the uploaded image
def process_image(image_path):
    config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    frozen_model = 'frozen_inference_graph.pb'
    
    # Tenserflow object detection model
    model = cv2.dnn_DetectionModel(frozen_model, config_file)

    # Reading Coco dataset
    classLabels = []
    with open('yolo3.txt', 'rt') as fpt:
        classLabels = fpt.read().rstrip('\n').split('\n')

    # Model training
    model.setInputSize(320, 320)
    model.setInputScale(1.0 / 127.5)
    model.setInputMean((127.5, 127.5, 127.5))
    model.setInputSwapRB(True)

    # Reading image
    img = cv2.imread(image_path)

    # Object detection
    ClassIndex, confidence, bbox = model.detect(img, confThreshold=0.5)

    # Plotting boxes
    font_scale = 3
    font = cv2.FONT_HERSHEY_PLAIN
    for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
        cv2.rectangle(img, boxes, (0, 255, 0), 3)
        cv2.putText(img, classLabels[ClassInd - 1], (boxes[0] + 10, boxes[1] + 40), font, fontScale=font_scale,
                    color=(0, 0, 255), thickness=3)

    # Save the processed image
    processed_image_path = os.path.join(UPLOAD_FOLDER, 'processed_image.jpg')
    cv2.imwrite(processed_image_path, img)

    return processed_image_path

@app.route('/process-image', methods=['POST'])
def process_uploaded_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the uploaded image
        processed_image_path = process_image(file_path)
        
        # Read the processed image file
        with open(processed_image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        return jsonify({'processed_image': encoded_image}), 200
    
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/processed-image')
def get_processed_image():
    processed_image_path = os.path.join(UPLOAD_FOLDER, 'processed_image.jpg')
    return send_file(processed_image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
