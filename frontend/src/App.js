import React, { useState } from 'react';
import axios from 'axios';
import './App.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCheck, faCloudArrowUp, faHome, faHourglassHalf, faMousePointer } from '@fortawesome/free-solid-svg-icons'

function App() {
  const [file, setFile] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [processing, setProcesing] = useState(false)

  const handleSubmit = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);
  }

  const handleRefresh=()=>{
    window.location.reload()
    setFile(null)
    setProcesing(false)
    setProcessedImage(null)
  }

  const handleImageUpload = async () => {

    setProcesing(true)

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5001/process-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response)
      setProcessedImage(`data:image/jpeg;base64, ${response.data.processed_image}`);
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
      <div className='text-center p-5 py-0'>
        <h1 className='m-4'>Image Processing App</h1>
        <div>
          <label for="upload-photo"><h2 className='text-secondary'>{(file) ? (processedImage) ? <><h1 className='text-success'>Done<FontAwesomeIcon className='mx-3' icon={faCheck} /></h1></> : (processing) ? <><h1>Processing....<FontAwesomeIcon className='mx-2' icon={faHourglassHalf} /></h1></> : <><FontAwesomeIcon className="mb-3" icon={faMousePointer} /><h1>Click to Process</h1></> : <><FontAwesomeIcon className='fa-2x' icon={faCloudArrowUp} /><h2>Upload Image</h2></>}</h2></label>
          <input type="file" accept="image/*" onChange={handleSubmit} id='upload-photo' />
        </div>
        <div className='text-center'>
          <button className='upload-btn ' onClick={handleImageUpload} style={{cursor:`${(!file)?"not-allowed":"pointer"}`}} disabled={!file}>{(processing) ? (processedImage) ? "COMPLETED": "PROCESSING..." : "PROCESS"}</button>
          <button className='upload-btn ' onClick={handleRefresh}>REFRESH</button>
        </div>
        <div className='row'>
          <div className='col-lg-6 my-4'> <h1>Original Image</h1> {file && <img className='image-block' src={URL.createObjectURL(file)} alt="Uploaded" style={{ width: '75%' }} />}</div>
          <div className='col-lg-6 my-4'> <h1>Processed Image</h1>{processedImage && <img className='image-block' src={processedImage} alt="Processed" style={{ width: '75%' }} />}</div>
        </div>
      </div>
    </>
  );
}

export default App;
