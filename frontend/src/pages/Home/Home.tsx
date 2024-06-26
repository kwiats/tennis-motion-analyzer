import React, { useState } from "react";
import FileUpload from "../../components/FileUpload/FileUpload.tsx";
import ProcessedFile from "../../components/ProcessedFile/ProcessedFile.tsx";
import "./Home.scss";

const Home: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [processedFileUrl, setProcessedFileUrl] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleFileUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("video", file);

    const response = await fetch("http://localhost:8000/video/upload_video", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (response.ok) {
      const downloadUrl = `http://localhost:8000/video/${data.output_path}`;
      setProcessedFileUrl(downloadUrl);
    } else {
      console.error(data.error);
    }
  };

  return (
    <div className="home-container">
      <h1>Upload and Process File</h1>
      <FileUpload
        onFileChange={handleFileChange}
        onFileUpload={handleFileUpload}
      />
      <ProcessedFile processedFileUrl={processedFileUrl} />
    </div>
  );
};

export default Home;
