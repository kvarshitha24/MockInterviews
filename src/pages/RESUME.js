import React, { useState } from "react";
import "./RESUME.css";

const RESUME = ({ onNext }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewURL, setPreviewURL] = useState(null);
  const [fileType, setFileType] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);

    if (file) {
      const fileExtension = file.name.split('.').pop().toLowerCase();
      setFileType(fileExtension);
      
      // Create a preview URL for image files
      if (file.type.startsWith('image/')) {
        const url = URL.createObjectURL(file);
        setPreviewURL(url);
      } else {
        setPreviewURL(null);
      }
    }
  };

  const handleUpdateResume = async () => {
    if (selectedFile) {
      alert(`Resume uploaded: ${selectedFile.name}`);
      const formData = new FormData();
      formData.append("resume", selectedFile);
      const response = await fetch('http://127.0.0.1:5000/resume', {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      console.log(result);
      const projects = JSON.stringify(result.projects);
      const technical_skills = JSON.stringify(result.technical_skills);
      localStorage.setItem('project', projects);
      localStorage.setItem('skills', technical_skills);
      onNext();
    } else {
      alert("Please select a file first.");
    }
  };

  return (
    <div className="resume-page">
      <div className="resume-content">
        <h1 className="resume-title">Upload Your Resume</h1>
        <p className="resume-subtitle">Select a file from your device or drag and drop it here</p>
        <div className="upload-section">
          <div className="upload-box">
            <input
              type="file"
              id="file-input"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />
            <div className="upload-instructions">
              {selectedFile ? (
                <span>{selectedFile.name}</span>
              ) : (
                <span>Drag and drop your file here</span>
              )}
            </div>
            <div className="upload-or">OR</div>
            <label htmlFor="file-input" className="upload-button">Select File</label>
          </div>
          <p className="accepted-formats">We accept DOC, PDF, JPEG, and JPG formats</p>
        </div>
        <button className="submit-resume-button" onClick={handleUpdateResume}>Submit</button>
      </div>
    </div>
  );
};

export default RESUME;
