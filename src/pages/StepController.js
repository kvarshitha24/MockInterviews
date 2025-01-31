import React, { useState } from "react";
import RESUME from "./RESUME";
import CHECK from "./CHECK";
import INSTRUCTIONS from "./INSTRUCTIONS";
import "./progressBar.css";

const StepController = () => {
  const [currentStep, setCurrentStep] = useState(1);

  const handleNextStep = () => {
    setCurrentStep((prevStep) => prevStep + 1);
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return <RESUME onNext={handleNextStep} />;
      case 2:
        return <INSTRUCTIONS onNext={handleNextStep} />;
      case 3:
        return <CHECK />;
      default:
        return <RESUME onNext={handleNextStep} />;
    }
  };

  return (
    <div className="step-controller">
      <div className="progress-bar">
        <div className={`step ${currentStep > 1 ? "completed" : currentStep === 1 ? "current" : ""}`}>
          Step 1: Resume Upload
        </div>
        <div className={`step ${currentStep > 2 ? "completed" : currentStep === 2 ? "current" : ""}`}>
          Step 2: Instructions 
        </div>
        <div className={`step ${currentStep > 3 ? "completed" : currentStep === 3 ? "current" : ""}`}>
          Step 3: Device Compatibility
        </div>
      </div>
      <div className="step-content">
        {renderStep()}
      </div>
    </div>
  );
};

export default StepController;
