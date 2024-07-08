import React from "react";

const UnitInput = ({ label, unit, value, onChange }) => {
  return (
    <div style={{ textAlign: "center", margin: "20px auto", width: "200px" }}>
      <h2>{label}</h2>
      <div style={{ display: "flex", alignItems: "center" }}>
        <input
          type="number"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          style={{ flex: 1, padding: "5px" }}
        />
        <span style={{ marginLeft: "10px" }}>{unit}</span>
      </div>
    </div>
  );
};

export default UnitInput;
