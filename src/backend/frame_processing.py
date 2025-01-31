import cv2
import torch
import numpy as np

# Load the YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

unauthorized_objects = ['cell phone', 'notebook', 'laptop']
person_class_id = 0
background_threshold = 0.5

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def process_frame(frame):
    nparr = np.frombuffer(frame, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    plain_background = is_plain_background(frame)
    unauthorized_detected, person_present, multiple_persons_detected = detect_objects(frame)
    gaze_direction = detect_eye_movement(frame)

    return {
        'plain_background': plain_background,
        'unauthorized_detected': unauthorized_detected,
        'person_present': person_present,
        'multiple_persons_detected': multiple_persons_detected,
        'gaze_direction': gaze_direction
    }

def is_plain_background(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    total_pixels = binary.shape[0] * binary.shape[1]
    background_pixels = cv2.countNonZero(binary)
    background_percentage = background_pixels / total_pixels
    return background_percentage >= background_threshold

def detect_objects(frame):
    results = model(frame)
    detected_objects = results.pandas().xyxy[0]
    warnings = detected_objects[detected_objects['name'].isin(unauthorized_objects)]
    persons_detected = detected_objects[detected_objects['class'] == person_class_id]
    multiple_persons_detected = len(persons_detected) > 1
    return not warnings.empty, not persons_detected.empty, multiple_persons_detected

def detect_eye_movement(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    gaze_direction = "Unknown"
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 1:
            eye_positions = []
            for (ex, ey, ew, eh) in eyes:
                eye_center = detect_iris(roi_gray[ey:ey+eh, ex:ex+ew])
                if eye_center:
                    eye_positions.append((eye_center[0] + ex, eye_center[1] + ey))
            if len(eye_positions) >= 1:
                gaze_direction = get_gaze_direction(eye_positions, w)
                break
    return gaze_direction

def get_gaze_direction(eye_positions, face_width):
    avg_eye_x = np.mean([pos[0] for pos in eye_positions])
    if avg_eye_x < face_width * 0.45 or avg_eye_x > face_width * 0.58:
        return "Not Looking Straight"
    else:
        return "Looking Straight"

def detect_iris(eye_region):
    _, thresh = cv2.threshold(eye_region, 30, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            return (cx, cy)
    return None
