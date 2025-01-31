import React, { useState, useRef, useEffect } from "react";
import "./CHECK.css";
import { Link } from "react-router-dom";

const CHECK = () => {
  const [audioChecked, setAudioChecked] = useState(false);
  const [videoChecked, setVideoChecked] = useState(false);
  const [testing, setTesting] = useState(false);
  const [cameraStream, setCameraStream] = useState(null);
  const videoRef = useRef(null);
  const [recordedAudio, setRecordedAudio] = useState(null);
  const audioRef = useRef(null);
  const [audioText, setAudioText] = useState("hello");
  const [verificationResult, setVerificationResult] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [startRecordingEnabled, setStartRecordingEnabled] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognizer = new SpeechRecognition();
  const finalTranscriptRef = useRef("");

  // Handle video check
  const handleVideoCheck = async () => {
    setTesting(true);
    try {
      console.log("Requesting camera access...");
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      setCameraStream(stream);
      console.log("Camera stream obtained:", stream);
    } catch (error) {
      console.error("Error accessing camera:", error);
      alert("Camera access denied or not available.");
      setTesting(false);
    }
  };

  // Capture photo from video feed
  const capturePhoto = () => {
    if (videoRef.current && cameraStream) {
      const canvas = document.createElement("canvas");
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      canvas.getContext("2d").drawImage(videoRef.current, 0, 0);
      const imageUrl = canvas.toDataURL("image/png");
      console.log("Photo captured:", imageUrl);
      alert("Photo captured!");
      setVideoChecked(true);
      setTesting(false);
      cameraStream.getTracks().forEach((track) => track.stop());
      setCameraStream(null);
    }
  };

  // Handle audio check
  const handleAudioCheck = async () => {
    setTesting(true);
    setDisplayText("Please read this text: 'hello'");
    setStartRecordingEnabled(true); // Enable start recording button
  };

  // Start recording audio
  const startRecording = () => {
    setTesting(true);
    setStartRecordingEnabled(false); // Disable start recording button during recording
    setIsRecording(true);
    recognizer.continuous = false;
    recognizer.interimResults = true;
    recognizer.lang = "en-US";

    recognizer.onresult = (event) => {
      let interimTranscript = "";
      let finalTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript + " ";
        } else {
          interimTranscript += event.results[i][0].transcript + " ";
        }
      }

      // Update verification result with final transcript
      finalTranscriptRef.current = finalTranscript.trim();
      console.log("Interim transcript:", interimTranscript);
    };

    recognizer.start();
  };

  // Stop recording audio
  const stopRecording = () => {
    recognizer.stop();
    setIsRecording(false);
  };

  // Effect to handle video ref assignment
  useEffect(() => {
    if (videoRef.current && cameraStream) {
      videoRef.current.srcObject = cameraStream;
      videoRef.current.onloadedmetadata = () => {
        videoRef.current.play();
        setTesting(false); // Enable "Capture Photo" button
      };
    }
  }, [cameraStream]);

  // Clean up on component unmount
  useEffect(() => {
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [cameraStream]);

  useEffect(() => {
    recognizer.onend = () => {
      console.log("Speech recognition ended.");
      console.log("Verification Result:", finalTranscriptRef.current);
      console.log("Expected Text:", audioText);

      if (finalTranscriptRef.current.toLowerCase() === audioText.toLowerCase()) {
        alert("Audio verification successful!");
        setAudioChecked(true);
        setTesting(false);
        setDisplayText(""); // Clear text after successful verification
      } else {
        alert("Audio verification failed. Please speak louder and clearer.");
        setDisplayText("Please read this text: 'The quick brown fox jumps over the lazy dog'");
        setStartRecordingEnabled(true); // Re-enable start recording button
        setTesting(false);
      }
    };

    recognizer.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      alert("Speech recognition encountered an error. Please try again.");
      setStartRecordingEnabled(true); // Re-enable start recording button on error
      setTesting(false);
    };
  }, [recognizer, audioText]);

  return (
    <div className="check-page">
      <div className="check-content">
        <h1 className="check-title">Device Compatibility Check</h1>
        <div className="check-section">
          <div className="equipment-check">
            <div className={`equipment-item ${videoChecked ? "checked" : ""}`}>
              <h3>Camera</h3>
              <button
                className="equipment-button"
                onClick={handleVideoCheck}
                disabled={testing || videoChecked}
              >
                {videoChecked ? "Checked" : "Check Camera"}
              </button>
              {cameraStream && (
                <div>
                  <video ref={videoRef} className="video" autoPlay playsInline />
                  <button
                    className="equipment-button"
                    onClick={capturePhoto}
                    disabled={videoChecked || testing}
                  >
                    Capture Photo
                  </button>
                </div>
              )}
            </div>
            <div className={`equipment-item ${audioChecked ? "checked" : ""}`}>
              <h3>Microphone</h3>
              <button
                className="equipment-button"
                onClick={handleAudioCheck}
                disabled={testing || audioChecked}
              >
                {audioChecked ? "Checked" : "Check Microphone"}
              </button>
              {(startRecordingEnabled || isRecording) && (
                <div>
                  <p>{displayText}</p>
                  {!isRecording ? (
                    <button
                      className="equipment-button"
                      onClick={startRecording}
                    >
                      Start Recording
                    </button>
                  ) : (
                    <button
                      className="equipment-button"
                      onClick={stopRecording}
                    >
                      Stop Recording
                    </button>
                  )}
                </div>
              )}
              {recordedAudio && (
                <div>
                  <audio ref={audioRef} className="audio" controls src={recordedAudio} />
                </div>
              )}
            </div>
          </div>
          <Link to="/interview">
            <button className="join-button" disabled={testing || !(videoChecked && audioChecked)}>
              {testing ? "Testing..." : "Start Interview"}
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default CHECK;
