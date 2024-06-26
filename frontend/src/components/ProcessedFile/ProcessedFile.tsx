import React from "react";
import "./ProcessedFile.scss";

interface ProcessedFileProps {
  processedFileUrl: string | null;
}

const ProcessedFile: React.FC<ProcessedFileProps> = ({ processedFileUrl }) => {
  return (
    <>
      {processedFileUrl && (
        <div className="processed-file-container">
          <h2>Processed File</h2>
          <video autoPlay loop>
            <source src={processedFileUrl} type="video/mp4" />
          </video>
        </div>
      )}
    </>
  );
};

export default ProcessedFile;
