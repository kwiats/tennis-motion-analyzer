import React, { useState } from "react";
import "./FileUpload.scss";

interface FileUploadProps {
  onFileChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onFileUpload: () => void;
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileChange,
  onFileUpload,
}) => {
  const [fileName, setFileName] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFileName(event.target.files[0].name);
      onFileChange(event); 
    }
  };

  return (
    <div className="file-upload-container">
      <input type="file" id="file-upload" onChange={handleFileChange} />
      <label htmlFor="file-upload">Choose File</label>
      {fileName && <p className="file-name">{fileName}</p>}
      <button onClick={onFileUpload}>Upload File</button>
    </div>
  );
};

export default FileUpload;
