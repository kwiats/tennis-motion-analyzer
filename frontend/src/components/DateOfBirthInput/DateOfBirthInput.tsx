import React, { useState } from "react";

const DateOfBirthInput = ({ onDateChange }) => {
  const [day, setDay] = useState("");
  const [month, setMonth] = useState("");
  const [year, setYear] = useState("");

  const handleDayChange = (e) => {
    const value = e.target.value;
    if (/^\d{0,2}$/.test(value)) {
      setDay(value);
      if (value.length === 2) {
        document.getElementById("month-input").focus();
      }
    }
  };

  const handleMonthChange = (e) => {
    const value = e.target.value;
    if (/^\d{0,2}$/.test(value)) {
      setMonth(value);
      if (value.length === 2) {
        document.getElementById("year-input").focus();
      }
    }
  };

  const handleYearChange = (e) => {
    const value = e.target.value;
    if (/^\d{0,4}$/.test(value)) {
      setYear(value);
      if (value.length === 4) {
        document.getElementById("year-input").blur();
      }
    }
  };

  const handleBlur = () => {
    if (day.length === 2 && month.length === 2 && year.length === 4) {
      const date = new Date(`${year}-${month}-${day}`);
      if (!isNaN(date)) {
        onDateChange(date);
      }
    }
  };

  return (
    <div style={{ textAlign: "center", margin: "20px auto", width: "100%" }}>
      <h2>Select Date of Birth</h2>
      <div>
        <input
          id="day-input"
          type="text"
          value={day}
          onChange={handleDayChange}
          onBlur={handleBlur}
          placeholder="DD"
          style={{ width: "50px", textAlign: "center", marginRight: "10px" }}
          maxLength={2}
        />
        <input
          id="month-input"
          type="text"
          value={month}
          onChange={handleMonthChange}
          onBlur={handleBlur}
          placeholder="MM"
          style={{ width: "50px", textAlign: "center", marginRight: "10px" }}
          maxLength={2}
        />
        <input
          id="year-input"
          type="text"
          value={year}
          onChange={handleYearChange}
          onBlur={handleBlur}
          placeholder="YYYY"
          style={{ width: "80px", textAlign: "center" }}
          maxLength={4}
        />
      </div>
    </div>
  );
};

export default DateOfBirthInput;
