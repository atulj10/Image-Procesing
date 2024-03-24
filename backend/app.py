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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def process_image(image_path):
    config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    frozen_model = 'frozen_inference_graph.pb'
    
    model = cv2.dnn_DetectionModel(frozen_model, config_file)

    classLabels = []
    with open('yolo3.txt', 'rt') as fpt:
        classLabels = fpt.read().rstrip('\n').split('\n')

    model.setInputSize(320, 320)
    model.setInputScale(1.0 / 127.5)
    model.setInputMean((127.5, 127.5, 127.5))
    model.setInputSwapRB(True)

    img = cv2.imread(image_path)

    ClassIndex, confidence, bbox = model.detect(img, confThreshold=0.5)

    font_scale = 3
    font = cv2.FONT_HERSHEY_PLAIN
    for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
        cv2.rectangle(img, boxes, (0, 255, 0), 3)
        label = classLabels[ClassInd - 1]
        print(f'Label: {label}, Number: {ClassInd}')
        cv2.putText(img, classLabels[ClassInd - 1], (boxes[0] + 10, boxes[1] + 40), font, fontScale=font_scale,
                    color=(0, 0, 255), thickness=3)

    processed_image_path = os.path.join(UPLOAD_FOLDER, 'processed_image.jpg')
    cv2.imwrite(processed_image_path, img)

    return processed_image_path,label,ClassInd

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
        
        processed_image_path, labels, label_counts = process_image(file_path)

        # print(f'In the outputLabel: {labels}, Number: {label_counts}')

    
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
    app.run(debug=True,port=5001)
