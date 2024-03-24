import React, { useState } from 'react';
import axios from 'axios';
import './App.css'

function App() {
  const [file, setFile] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleImageUpload = async (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:5001/process-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response)
      setProcessedImage(`data:image/jpeg;base64, ${response.data.processed_image}`); // Set processed image
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };


  return (
    <>
      <nav class="navbar navbar-expand-lg bg-body-secondary ">
        <div class="container-fluid" >
          <a class="navbar-brand" href="#">Navbar</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
              <a class="nav-link active" aria-current="page" href="#">Home</a>
              <a class="nav-link" href="#">Page1</a>
              <a class="nav-link" href="#">Page2</a>
            </div>
          </div>
        </div>
      </nav>
      <div className='text-center p-5'>
        <h1 className='m-4'>Image Processing App</h1>
        <div>
          <label for="upload-photo"><h2 className='text-secondary'>{file ? `${processedImage? "Done ✔️" : "Processing image....."}`:"Browse File"}</h2></label>
          <input className=' m-3' type="file" accept="image/*" onChange={handleImageUpload} id='upload-photo' />
        </div>
        <div className='row'>
          <div className='col-lg-6 my-4'> <h1>Original Image</h1> {file && <img src={URL.createObjectURL(file)} alt="Uploaded" style={{ width: '75%' }} />}</div>
          <div className='col-lg-6 my-4'> <h1>Processed Image</h1>{processedImage && <img src={processedImage} alt="Processed" style={{ width: '75%' }} />}</div>
        </div>
      </div>
    </>
  );
}

export default App;
