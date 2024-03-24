
# Image Processing Web Application

This is a web application for image processing using Flask for the backend and React for the frontend.


## Setup Instructions
#### 1 Clone the Repository:

```http
  git clone https://github.com/atulj10/Image-Procesing.git
```

#### 2 Backend Setup:
-Navigate to the backend directory:

```http
  cd backend
```
-Install Python dependencies:

```http
  pip install -r requirements.txt
```

#### 3 Frontend Setup:
-Navigate to the frontend directory:

```http
  cd frontend
```

-Install Node.js dependencies:

```http
  npm install
```


## Running the Applicaton

### 1. Start the Backend Server :

- From the `backend` directory, run:
```http
  python app.py
```
 - The Flask backend will start running on http://localhost:5001.

 ### 2. Start the Frontend Development Server :

- From the `frontend` directory, run:
```http
  npm start
```
 - The React frontend will start running on http://localhost:3000.

### 3. Accessing the Application:

- Open your web browser and navigate to http://localhost:3000 to access the image processing application.

## Usage

- Upload an image using the provided file input.
- Click on the "Process" button to process the uploaded image.
- The processed image will be displayed along with object detection labels if any.
- You can refresh the page to upload a new image.


## Author

- Atul Anand


## License

- This project is licensed under the MIT License.

