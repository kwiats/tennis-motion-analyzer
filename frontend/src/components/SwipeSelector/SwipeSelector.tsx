import React, { useState, useEffect } from "react";
import { useSwipeable } from "react-swipeable";

const SwipeSelector = ({ title, items, onSelectionChange }) => {
  const [selectedIndex, setSelectedIndex] = useState(0);

  useEffect(() => {
    if (onSelectionChange) {
      onSelectionChange(items[selectedIndex]);
    }
  }, [selectedIndex, items, onSelectionChange]);

  const handleSwipedLeft = () => {
    setSelectedIndex((prevIndex) => (prevIndex + 1) % items.length);
  };

  const handleSwipedRight = () => {
    setSelectedIndex(
      (prevIndex) => (prevIndex - 1 + items.length) % items.length
    );
  };

  const handlers = useSwipeable({
    onSwipedLeft: handleSwipedLeft,
    onSwipedRight: handleSwipedRight,
    preventDefaultTouchmoveEvent: true,
    trackMouse: true,
  });

  return (
    <div
      {...handlers}
      style={{
        textAlign: "center",
        padding: "20px",
        border: "1px solid #ccc",
        width: "100%",
        margin: "0 auto",
      }}
    >
      <h2>{title}</h2>
      <div style={{ fontSize: "24px", fontWeight: "bold" }}>
        {items[selectedIndex]}
      </div>
      <p>Swipe left or right to change</p>
    </div>
  );
};

export default SwipeSelector;
