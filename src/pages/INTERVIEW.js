
import React, { useState, useEffect, useRef, useContext } from 'react';
import './INTERVIEW.css';
import axios from 'axios';
import io from 'socket.io-client';
import { logincontext } from "../contexts/Logincontext";

const socket = io('http://127.0.0.1:5000', {
  transports: ['websocket', 'polling']
});
const videoConstraints = {
  width: 1280,
  height: 720,
  facingMode: 'user',
};

const INTERVIEW = () => {
  const [currentuser,loginerror,UserloginStatus,Loginuser,Logoutuser,isUser,isRecruiter,isAdmin] = useContext(logincontext);
  const [recording, setRecording] = useState(false);
  const [timer, setTimer] = useState(0);
  const [submitted, setSubmitted] = useState(false);
  const [welcomeMessage, setWelcomeMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [showQuestions, setShowQuestions] = useState(false);
  const [countdown, setCountdown] = useState(50);
  const videoRef = useRef(null);
  const [question, setQuestion] = useState("");
  const [readingTime, setReadingTime] = useState(false);
  const [thankYouMessage, setThankYouMessage] = useState("");
  const [videourl , setVideourl] = useState(null);
  const [answer, setAnswer] = useState("");
  const [showAnswer, setShowAnswer] = useState(false);
  const [answerCountdown, setAnswerCountdown] = useState(50);
  const [prevAnswer, setPrevAnswer] = useState("")
  const [flag, setFlag] = useState(false);
  const canvasRef = useRef(null);
  const [videoStream, setVideoStream] = useState(null);

// Function to capture video frame
const captureFrame = () => {
  const canvas = canvasRef.current;
  const video = videoRef.current;
  if (canvas && video) {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const frame = canvas.toDataURL('image/jpeg');
    const binary = atob(frame.split(',')[1]);
    const array = [];
    for (let i = 0; i < binary.length; i++) {
      array.push(binary.charCodeAt(i));
    }
    const blob = new Blob([new Uint8Array(array)], { type: 'image/jpeg' });

    // Emit the frame to the server
    socket.emit('frame', blob);
  }
};

useEffect(() => {
  socket.on('frame_response', (data) => {
    console.log('Proctoring Data:', data);
    
    if (data.unauthorized_detected) {
      alert("Unauthorized object detected!");
    }
    if(!data.person_present){
      alert("No person detected!");
    }
    if(data.multiple_persons_detected){
      alert("Multiple persons detected!");
    }
  });

  return () => {
    socket.off('frame_response');
  };
}, []);

// Start webcam stream on component mount
useEffect(() => {
  navigator.mediaDevices
    .getUserMedia({ video: videoConstraints })
    .then(stream => {
      videoRef.current.srcObject = stream;
      setVideoStream(stream);
    })
    .catch(error => {
      console.error('Error accessing the camera', error);
    });

  return () => {
    if (videoStream) {
      videoStream.getTracks().forEach(track => track.stop());
    }
  };
}, []);

useEffect(() => {
  // Start capturing frames at regular intervals if recording
  let frameInterval;
  frameInterval = setInterval(() => {
    captureFrame();
  }, 1000); // Capture frames every second
  return () => clearInterval(frameInterval);
}, [timer,countdown,answerCountdown]);
  
  useEffect(() => {
    if (!currentuser) return;
    const { first_name, last_name } = currentuser;
    const encodedFullName = encodeURIComponent(
      `${first_name?.trim() || ''} ${last_name?.trim() || ''}`
    );

    axios.get(`http://127.0.0.1:5000/welcome_message`, {
      params: {
        user: encodedFullName
      }
    })
      .then(response => {
        setWelcomeMessage(response.data.message);
        setIsLoading(false);
        axios.get("http://127.0.0.1:5000/questions", {
            params: {
              user: encodedFullName
            }
          })
          .then(response => {
            setQuestion(response.data.message);
            setVideourl(response.data.video);
          })
          .catch(error => {
            console.error('Error fetching question:', error);
          });
      })
      .catch(error => {
        console.error('Error fetching welcome message:', error);
        setIsLoading(false);
      });

    const welcomeTimer = setInterval(() => {
      setCountdown(prev => {
        if (prev > 1) {
          return prev - 1;
        } else {
          
          setShowQuestions(true);
          setCountdown(100);
          
          clearInterval(welcomeTimer);
        }
      });
    }, 1000);

    return () => clearInterval(welcomeTimer);
  }, [currentuser]);

  useEffect(() => {
    let interval;
    if (recording) {
      interval = setInterval(() => {
        setTimer(prev => prev + 1);
        captureFrame();
      }, 1000);
    } else {
      setTimer(0);
    }

    if (timer >= 120) {
      stopRecording();
    }
    return () => clearInterval(interval);
  }, [recording, timer]);

  const startRecording = () => {
    
    setRecording(true);
    setSubmitted(false);
    setReadingTime(false);

    // setRecording(true);
    // setTimer(0);
    // setSubmitted(false);
    // setShowQuestions(true);

    axios.post('http://127.0.0.1:5000/start_recording')
      .then(response => {
        console.log('Recording started:', response.data);
      })
      .catch(error => {
        console.error('Error starting recording:', error);
      });
  };

  const stopRecording = () => {
    
    setRecording(false);
    setSubmitted(true);
    setReadingTime(false);
    setShowAnswer(true); // Show the answer input field
    setCountdown(100);
    
    setFlag(true);
    axios.post('http://127.0.0.1:5000/stop_recording',{
        ques:question
    })
      .then(response => {
        console.log('Recording stopped and transcribed:', response.data);
        setAnswer(response.data.answer);
        setFlag(false)
        setAnswerCountdown(40)
      axios.get("http://127.0.0.1:5000/questions")
      .then(response => {
          if (response.data.message === 'end') {
            if (!showAnswer){
            axios.get(`http://127.0.0.1:5000/thank`, {
              params: {
              user: encodeURIComponent(`${currentuser.first_name} ${currentuser.last_name}`)
              }
             })
            .then(response => {
            setThankYouMessage(response.data.message);
            })
            .catch(error => {
            console.error('Error fetching thank you message:', error);
            });

            axios.get(`http://127.0.0.1:5000/analyse`)
            .then(response => {
            console.log("Doneeee");
            })
            .catch(error => {
            console.error('Error fetching thank you message:', error);
            });
          }

          } else{
            setQuestion(response.data.message);
            setVideourl(response.data.video);
            setReadingTime(true);
            setCountdown(100);
            setSubmitted(false);
            setRecording(false);
            setTimer(0);
         }
        })
        .catch(error => {
          console.error('Error fetching question:', error);
        });
 
        const answerTimer = setInterval(() => {
          setAnswerCountdown(prev => {
            if (prev > 1) {
              return prev - 1;
            } else {
              // After 30 seconds, submit the answer and hide the input field
              submitAnswer();
              setShowAnswer(false);
              clearInterval(answerTimer);
              return 0;
            }
          });
        }, 1000);
      })
      .catch(error => {
        console.error('Error stopping recording:', error);
      });

}

  const submitAnswer = () => {
    console.log(answer);
    
    
  };

 

  

  
  useEffect(() => {
    if (countdown > 0 && showQuestions && !recording) {
      const readingTimer = setTimeout(() => {
        setCountdown(prev => prev - 1);
      }, 1000);

      if (countdown === 1) {
        startRecording();
      }

      return () => clearTimeout(readingTimer);
    }
  }, [countdown, showQuestions, recording]);

  const videoReff = useRef(null);

    useEffect(() => {
      if (!videourl) return;
      const video = videoReff.current;

      const handleVideoEnd = () => {
        // Logic to handle what happens when the video ends, if any
      };

      // video.addEventListener('ended', handleVideoEnd);

      return () => {
        // video.removeEventListener('ended', handleVideoEnd);
      };
    }, [videourl]);

    const handleReload = () => {
      if (videoReff.current) {
        videoReff.current.currentTime = 0;
        videoReff.current.play();
      }
    };

  return (
    <div className="interview">
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        thankYouMessage ? (
          <div className="welcome-message">
            <h1>{thankYouMessage}</h1>
          </div>
        ) : (
          showQuestions ? (
            <>
              <div className="interview-body">
                  {showAnswer ? (
                  flag ? (
                    // Show loading spinner when flag is true
                    <div className="loading-symbol"></div>
                  ) : (
                    // Show answer edit container when flag is false
                    <div className="answer-edit-container">
                      <textarea 
                        value={answer} 
                        onChange={(e) => setAnswer(e.target.value)} 
                        className="answer-textarea" 
                      />
                      <p className="answer-timer">Time left to edit: {answerCountdown}s</p>
                      <button onClick={submitAnswer} className="submit-answer-button">
                        Submit Answer
                      </button>
                      
                    </div>
                  )
                ): (
                  <div className="question-container">
                    <div className="main-video-container">
                      <video
                        ref={videoReff}
                        src={videourl}
                        autoPlay
                        controls={false}
                        className="main-video"
                      />
                      <div className="question-overlay">
                        <p className="question-text">{question}</p>
                      </div>
                      <div className="reload-button-container">
                        <button onClick={handleReload}>Reload</button>
                      </div>
                      <div className="recording-container">
                        <button onClick={recording ? stopRecording : startRecording} disabled={submitted} className={`mic-button ${recording ? 'recording' : submitted ? 'submitted' : ''}`}>
                          {recording ? 'Stop Recording' : submitted ? 'Submitted' : 'Start Recording'}
                        </button>
                        <div className="timer">{recording && !submitted ? timer : ''}</div>
                      </div>
                        
                    </div>
                  </div>
                )}
                {!recording && !showAnswer && question !== "Analysing your answer...." && (
                  <p className="reading-timer">Time left to read: {countdown}s</p>
                )}
              </div>
            </>
          ) : (
            <div className="welcome-message">
              <h1>{welcomeMessage}</h1>
              <p className="welcome-timer">Time left: {countdown}s</p>
            </div>
          )
        )
      )}
      <video ref={videoRef} className="canvas-bottom-right"  autoPlay muted  />
      <canvas ref={canvasRef} className='canvas' ></canvas>
    </div>
  );
};

export default INTERVIEW;

