import React from "react";
import "./INSTRUCTIONS.css";

const INSTRUCTIONS = ({ onNext }) => {
  const handleContinue = () => {
    onNext();
  };
  return (
    <div className="instructions-page">
      <div className="instructions-content">
        <h1 className="instructions-title">Instructions for Online Interview</h1>
        <ul className="instructions-list">
          <li>This is a web-proctored test.</li>
          <li>Questions will be asked by AI.</li>
          <li>Sit in a well-lit place with good lighting.</li>
          <li>Your background should be plain.</li>
          <li>No malpractices are allowed.</li>
          <li>Ensure your internet connection is stable.</li>
          <li>Use a device with a working camera and microphone.</li>
          <li>Wear professional attire.</li>
          <li>Be in a quiet environment.</li>
          <li>Follow the instructions provided during the interview.</li>
          <li>Avoid any distractions or interruptions.</li>
          <li>Ensure your device is fully charged or plugged in.</li>
          <li>Test your audio and video before starting the interview.</li>
          <li>Be punctual and join the interview on time.</li>
        </ul>
        <button className="continue-button" onClick={handleContinue}>Continue</button>
      </div>
    </div>
  );
};

export default INSTRUCTIONS;