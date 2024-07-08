import React from "react";

const TextInput = ({ label, value, onChange }) => {
  return (
    <div style={{ textAlign: "center", margin: "20px auto", width: "300px" }}>
      <h2>{label}</h2>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{ width: "100%", padding: "10px", boxSizing: "border-box" }}
      />
    </div>
  );
};

export default TextInput;
