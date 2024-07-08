import React, { useState } from "react";
import FileUpload from "../../components/FileUpload/FileUpload.tsx";
import ProcessedFile from "../../components/ProcessedFile/ProcessedFile.tsx";
import "./Home.scss";
import { uploadFile } from "../../services/fileService.ts";
import SwipeSelector from "../../components/SwipeSelector/SwipeSelector.tsx";
import DateOfBirthInput from "../../components/DateOfBirthInput/DateOfBirthInput.tsx";
import UnitInput from "../../components/UnitInput/Unitinput.tsx";
import TextInput from "../../components/TextInput/TextInput.tsx";

const Home: React.FC = () => {
  const [selectedGender, setSelectedGender] = useState("👨 Male");
  const [selectedTechnique, setSelectedTechnique] = useState("serve");
  const [weight, setWeight] = useState("");
  const [height, setHeight] = useState("");
  const [dateOfBirth, setDateOfBirth] = useState(null);
  const [name, setName] = useState("");

  const [file, setFile] = useState<File | null>(null);
  const [processedFileUrl, setProcessedFileUrl] = useState<string | null>(null);
  const genderItems = ["👨 Male", "👩 Female"];
  const tennisTechniques = ["serve", "forehand", "backhand"];
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleSelectionTechniqueChange = (selectedItem: string) => {
    setSelectedTechnique(selectedItem);
  };

  const handleSelectionChange = (selectedItem: string) => {
    setSelectedGender(selectedItem);
  };

  const handleDateChange = (date: any) => {
    console.log(date);
    setDateOfBirth(date);
  };

  const handleUploadResponse = async (response: Response) => {
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error);
    }

    const data = await response.json();
    const downloadUrl = `${import.meta.env.VITE_API_URL}video/${
      data.output_path
    }`;
    setProcessedFileUrl(downloadUrl);
  };

  const handleFileUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("video", file);

    const response = await uploadFile(file);
    await handleUploadResponse(response);
  };

  return (
    <div className="home-container">
      <TextInput label="What's your name?" value={name} onChange={setName} />
      <SwipeSelector
        title={"Select your gender"}
        items={genderItems}
        onSelectionChange={handleSelectionChange}
      />
      <DateOfBirthInput onDateChange={handleDateChange} />
      <SwipeSelector
        title={"Select your techqniue"}
        items={tennisTechniques}
        onSelectionChange={handleSelectionTechniqueChange}
      />
      <UnitInput
        label="Your weight"
        unit="kg"
        value={weight}
        onChange={setWeight}
      />
      <UnitInput
        label="Your height"
        unit="cm"
        value={height}
        onChange={setHeight}
      />
      <div
        className="summary"
        style={{ marginTop: "20px", textAlign: "center" }}
      >
        <h2>Summary of Your Details</h2>
        <p>
          <strong>Name:</strong> {name}
        </p>
        <p>
          <strong>Gender:</strong> {selectedGender}
        </p>
        <p>
          <strong>Date of Birth:</strong>{" "}
          {dateOfBirth ? dateOfBirth.toLocaleDateString() : "Not set"}
        </p>
        <p>
          <strong>Technique:</strong> {selectedTechnique}
        </p>
        <p>
          <strong>Weight:</strong> {weight} kg
        </p>
        <p>
          <strong>Height:</strong> {height} cm
        </p>
      </div>
      <div className="title">
        <h1>Upload and Process File</h1>
      </div>
      <FileUpload
        onFileChange={handleFileChange}
        onFileUpload={handleFileUpload}
      />
      <ProcessedFile processedFileUrl={processedFileUrl} />
    </div>
  );
};

export default Home;
