from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from pymongo import MongoClient, errors
from werkzeug.security import check_password_hash, generate_password_hash
import re
import inter
import frame_processing
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os
import wave
import pyaudio
import threading
import time
import speech_recognition as sr
import requests,time
import analysis
import ssl

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")
uri = "mongodb+srv://katepallyvarshitha03:4WRAK6oVvvZI4bV8@cluster0.z4l6zvm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
global ans
ans = ""

try:
    client = MongoClient(uri)
    client.admin.command('ismaster')
    print("Connected to the database successfully.")
except errors.ConnectionFailure:
    print("Failed to connect to the database.")


db = client['MockInterviews']
users_collection = db['UsersDetails']
resume_collection = db['ResumeDetails']
recruiter_collection=db['Check_list']
main_recruiters_collection = db['Recruiters']



@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    print(data)

    # Retrieve form data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    role = data.get('role')  # Fetch the role from the request

    # Additional fields for recruiter
    
    # Check if the email already exists
    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'User already exists'}), 409

    # Hash the password
    password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Create common user data with role
    user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password_hash': password_hash,
        'role': role
    }

    # Role-based logic: If recruiter, add to Check_list; if user, add to UsersDetails
    if role == 'recruiter':
        company_name = data.get('company_name')
        recruiter_id = data.get('id')
        if not company_name or not recruiter_id:
            return jsonify({'error': 'Company name and ID are required for recruiters'}), 400

        # Insert recruiter details into Check_list collection
        user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password_hash': password_hash,
        'role': role,
        'company_name': company_name,
        'recruiter_id': recruiter_id,
    }
      
        recruiter_collection.insert_one(user_data)  # Insert recruiter into Check_list

    elif role == 'user':
        # Insert user details into UsersDetails collection
        user_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password_hash': password_hash,
        'role': role
    }
        users_collection.insert_one(user_data)  # Insert user into UsersDetails

    # Insert the common user data into the users collection


    return jsonify({'message': 'User created successfully'}), 201


private_key = RSA.import_key(open('/Users/surya/Documents/MockInterviews/src/backend/private.pem').read())
def decrypt_password(encrypted_password):
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_password = cipher.decrypt(base64.b64decode(encrypted_password))
    return decrypted_password.decode('utf-8')

global_mail=""
@app.route('/login', methods=['POST'])
def login():
    global global_mail
    data = request.get_json()
    email = data.get('mail')
    global_mail = email
    encrypted_password = data.get('password')
    role = data.get('role')  # Retrieve the role from the request
    
    if role=="admin":
        return jsonify({'message': 'Login successful', 'user': {'role': "admin"}}), 200
        

    print(data)
    
    # Decrypt the password
    try:
        password = decrypt_password(encrypted_password)
    except Exception as e:
        return jsonify({'error': 'Decryption failed'}), 400
    
    # Check if email, password, and role are provided
    if not email or not password or not role:
        return jsonify({'error': 'email, password, and role are required'}), 400
    
    
    
    # Find the user by email
    if role=="user":
        user = users_collection.find_one({'email': email})
    elif role=="recruiter":
        user = main_recruiters_collection.find_one({'email': email})
    
    # Check if the user exists, if password is correct, and if the role matches
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if user.get('role') != role:  # Check if the role matches
        return jsonify({'error': f'Invalid role: expected {user.get("role")}, got {role}'}), 403

    # Login successful
    return jsonify({
        'message': 'Login successful', 
        'user': {
            'first_name': user['first_name'], 
            'last_name': user['last_name'], 
            'email': user['email'], 
            'role': user['role']  # Send the user's role in the response
        }
    }), 200

@app.route('/profile', methods=['GET'])
def get_profile():
    # Assuming you have authenticated the user and have their email available
    email = request.args.get('email')  # Get email from query parameter or session
    role=request.args.get('role')
    if role=="user":
        user = users_collection.find_one({'email': email})
    elif role=="recruiter":
        user = main_recruiters_collection.find_one({'email': email})
    user = convert_objectid(user)
    print(user)
    if user:
        return jsonify({'data':user})
    else:
        return jsonify({'error': 'User not found'})
    
@app.route('/editprofile', methods=['POST'])
def edprofile():
    data = request.get_json()
    email = data.get('email')
    update_data = data.get('data')
    print(update_data)
    update_data = {k: v for k, v in update_data.items() if v is not None}
    if not update_data:
        return jsonify({'error': 'No valid fields to update'})
    try:
        result = users_collection.update_one({'email': email}, {'$set': update_data})
        if result.modified_count == 0:
            return jsonify({'error': 'No profile found to update'})
        return jsonify({'message': 'Profile updated successfully'})
    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({'error': 'An error occurred while updating the profile'})
    
res_data={}
total_data={}
@app.route('/resume', methods=['POST'])
def resume():
    global res_data,total_data
    text=inter.upload_file()
    res_data=text
    print("################################################################")
    print(res_data)
    total_data=res_data
    return text

@app.route('/welcome_message',methods=['GET'])
def welcome_message():
    name = request.args.get('user')
    print(name)
    msg = inter.greet(name)
    return jsonify({'message': msg})


def convert_objectid(user):
    if user and '_id' in user:
        user['_id'] = str(user['_id'])
    return user

@app.route('/user', methods=['POST'])
def check():
    data = request.get_json()
    email = data.get('mail')
    password = data.get('password')
    user = users_collection.find_one({'email': email})
    if user and check_password_hash(user['password_hash'], password):
        user = convert_objectid(user)
        user.pop('password_hash')  
        return jsonify({'status': 'success', 'data': user})
    else:
        return jsonify({'status': 'failure', 'message': 'Invalid credentials'})

def fun(q):
    url = "https://api.d-id.com/clips"
    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-IN-NeerjaNeural"
            },
            "ssml": "false",
            "input": q,
            },
        "config": { "result_format": "mp4" },
        "presenter_config": { "crop": { "type": "wide" } },
        "presenter_id": "amy-Aq6OmGZnMt",
        "driver_id": "Vcq0R4a8F0"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJvZHVjdF9pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vc3RyaXBlX2N1c3RvbWVyX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJvZHVjdF9uYW1lIjoidHJpYWwiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9zdWJzY3JpcHRpb25faWQiOiIiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9iaWxsaW5nX2ludGVydmFsIjoibW9udGgiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9wbGFuX2dyb3VwIjoiZGVpZC10cmlhbCIsImh0dHBzOi8vZC1pZC5jb20vc3RyaXBlX3ByaWNlX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJpY2VfY3JlZGl0cyI6IiIsImh0dHBzOi8vZC1pZC5jb20vY2hhdF9zdHJpcGVfc3Vic2NyaXB0aW9uX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jaGF0X3N0cmlwZV9wcmljZV9jcmVkaXRzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jaGF0X3N0cmlwZV9wcmljZV9pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vcHJvdmlkZXIiOiJnb29nbGUtb2F1dGgyIiwiaHR0cHM6Ly9kLWlkLmNvbS9pc19uZXciOmZhbHNlLCJodHRwczovL2QtaWQuY29tL2FwaV9rZXlfbW9kaWZpZWRfYXQiOiIyMDI0LTA5LTE4VDEwOjEzOjAzLjA2NFoiLCJodHRwczovL2QtaWQuY29tL29yZ19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vYXBwc192aXNpdGVkIjpbIlN0dWRpbyJdLCJodHRwczovL2QtaWQuY29tL2N4X2xvZ2ljX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jcmVhdGlvbl90aW1lc3RhbXAiOiIyMDI0LTA5LTE4VDEwOjExOjUwLjY5NFoiLCJodHRwczovL2QtaWQuY29tL2FwaV9nYXRld2F5X2tleV9pZCI6InJpMzBlZDkxd2giLCJodHRwczovL2QtaWQuY29tL3VzYWdlX2lkZW50aWZpZXJfa2V5IjoidThUclJzMllRRURHQnAtNjBvdXdYIiwiaHR0cHM6Ly9kLWlkLmNvbS9oYXNoX2tleSI6ImwtM0VjaExoa05VQjlCaTFrVlRCTiIsImh0dHBzOi8vZC1pZC5jb20vcHJpbWFyeSI6dHJ1ZSwiaHR0cHM6Ly9kLWlkLmNvbS9lbWFpbCI6InN1cnlhdGVqYWNod2FwcEBnbWFpbC5jb20iLCJodHRwczovL2QtaWQuY29tL3BheW1lbnRfcHJvdmlkZXIiOiJzdHJpcGUiLCJpc3MiOiJodHRwczovL2F1dGguZC1pZC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDEzMDA2MDA0OTAxOTg4MDQ3MzciLCJhdWQiOlsiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MjY2NTQ0MjgsImV4cCI6MTcyNjc0MDgyOCwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCByZWFkOmN1cnJlbnRfdXNlciB1cGRhdGU6Y3VycmVudF91c2VyX21ldGFkYXRhIG9mZmxpbmVfYWNjZXNzIiwiYXpwIjoiR3pyTkkxT3JlOUZNM0VlRFJmM20zejNUU3cwSmxSWXEifQ.NghadGW4JVLD2QWq2DXsIGy7fOTelAshxdmPsAoj2xV8IDuAVT1aChDpVbcpmNH5ZLeu7Y72ZfwDjYdcDDj6f2zT3KDjxy4ekc9DsyOODkcCmWm_SCNlvCPRgOJdaOUFG_-jguoHw8M_YOap6qsabSELzWwBiZJFa1QT6HbEYmMudDT3sjvKGVmG38AmJcBtpUFHthZJFsYAwWTxI0IASMRvtn4fgovfGvZfyrphFaQ6-eK1B12pkghL5EAkjcgo7PJm45GwGXo0A33ml9ypC87WxXwPGAHo59GKb4OaVSFXXLI79mL4cI-5BwmGXbth4z7FEOEOxf4ke8fYTt9uxQ"

    }

    response = requests.post(url, json=payload, headers=headers)
    response=response.json()
    print("KII")
    print(response)
    print("HIII")
    
    id=response["id"]
    print(id)
    time.sleep(40)
    url = "https://api.d-id.com/clips/"+id
    print(url)
    headers = {
        "accept": "application/json",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJvZHVjdF9pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vc3RyaXBlX2N1c3RvbWVyX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJvZHVjdF9uYW1lIjoidHJpYWwiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9zdWJzY3JpcHRpb25faWQiOiIiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9iaWxsaW5nX2ludGVydmFsIjoibW9udGgiLCJodHRwczovL2QtaWQuY29tL3N0cmlwZV9wbGFuX2dyb3VwIjoiZGVpZC10cmlhbCIsImh0dHBzOi8vZC1pZC5jb20vc3RyaXBlX3ByaWNlX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfcHJpY2VfY3JlZGl0cyI6IiIsImh0dHBzOi8vZC1pZC5jb20vY2hhdF9zdHJpcGVfc3Vic2NyaXB0aW9uX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jaGF0X3N0cmlwZV9wcmljZV9jcmVkaXRzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jaGF0X3N0cmlwZV9wcmljZV9pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vcHJvdmlkZXIiOiJnb29nbGUtb2F1dGgyIiwiaHR0cHM6Ly9kLWlkLmNvbS9pc19uZXciOmZhbHNlLCJodHRwczovL2QtaWQuY29tL2FwaV9rZXlfbW9kaWZpZWRfYXQiOiIyMDI0LTA5LTE4VDEwOjEzOjAzLjA2NFoiLCJodHRwczovL2QtaWQuY29tL29yZ19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vYXBwc192aXNpdGVkIjpbIlN0dWRpbyJdLCJodHRwczovL2QtaWQuY29tL2N4X2xvZ2ljX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jcmVhdGlvbl90aW1lc3RhbXAiOiIyMDI0LTA5LTE4VDEwOjExOjUwLjY5NFoiLCJodHRwczovL2QtaWQuY29tL2FwaV9nYXRld2F5X2tleV9pZCI6InJpMzBlZDkxd2giLCJodHRwczovL2QtaWQuY29tL3VzYWdlX2lkZW50aWZpZXJfa2V5IjoidThUclJzMllRRURHQnAtNjBvdXdYIiwiaHR0cHM6Ly9kLWlkLmNvbS9oYXNoX2tleSI6ImwtM0VjaExoa05VQjlCaTFrVlRCTiIsImh0dHBzOi8vZC1pZC5jb20vcHJpbWFyeSI6dHJ1ZSwiaHR0cHM6Ly9kLWlkLmNvbS9lbWFpbCI6InN1cnlhdGVqYWNod2FwcEBnbWFpbC5jb20iLCJodHRwczovL2QtaWQuY29tL3BheW1lbnRfcHJvdmlkZXIiOiJzdHJpcGUiLCJpc3MiOiJodHRwczovL2F1dGguZC1pZC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDEzMDA2MDA0OTAxOTg4MDQ3MzciLCJhdWQiOlsiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MjY2NTQ0MjgsImV4cCI6MTcyNjc0MDgyOCwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCByZWFkOmN1cnJlbnRfdXNlciB1cGRhdGU6Y3VycmVudF91c2VyX21ldGFkYXRhIG9mZmxpbmVfYWNjZXNzIiwiYXpwIjoiR3pyTkkxT3JlOUZNM0VlRFJmM20zejNUU3cwSmxSWXEifQ.NghadGW4JVLD2QWq2DXsIGy7fOTelAshxdmPsAoj2xV8IDuAVT1aChDpVbcpmNH5ZLeu7Y72ZfwDjYdcDDj6f2zT3KDjxy4ekc9DsyOODkcCmWm_SCNlvCPRgOJdaOUFG_-jguoHw8M_YOap6qsabSELzWwBiZJFa1QT6HbEYmMudDT3sjvKGVmG38AmJcBtpUFHthZJFsYAwWTxI0IASMRvtn4fgovfGvZfyrphFaQ6-eK1B12pkghL5EAkjcgo7PJm45GwGXo0A33ml9ypC87WxXwPGAHo59GKb4OaVSFXXLI79mL4cI-5BwmGXbth4z7FEOEOxf4ke8fYTt9uxQ"
    }

    response = requests.get(url, headers=headers).json()
    print(response)
    url = response["result_url"]
    print(url)
    return url

chk=0
prevQuestion=""
ans="JIi"
@app.route('/questions', methods=['GET'])
def interviewques():
    global ans,chk,TQandA,BQandA,prevQuestion
    
    while not ans:
        pass
    que,chk=inter.project_inter(ans)
    print(que,"***")
    prevQuestion=que
    print(TQandA)
    print("-------------------------")
    print(BQandA)
    url = fun(que)
    # url = "/Users/surya/Downloads/amy-Aq6OmGZnMt (3).mp4"
    # url="https://www.youtube.com/watch?v=kOctZPPv2Bg"
    
    # url="https://d-id-clips-prod.s3.us-west-2.amazonaws.com/google-oauth2%7C110547750606485205798/clp_JesAbjhj37Yvj2h_KIew_/amy-Aq6OmGZnMt.mp4?AWSAccessKeyId=AKIA5CUMPJBIJ7CPKJNP&Expires=1725719081&Signature=TSePOHIzqu8fIapS7k9zwpMwxnY%3D"
    print("Url :",url)
    return jsonify({'message': que, 'video':url})


@app.route('/thank', methods=['GET'])
def thank():
    global TQandA,BQandA
    print("************Thanku*********")
    print(TQandA)
    print(BQandA)
    return jsonify({'message':inter.end()})

@socketio.on('frame')
def handle_frame(blob):
    try:
        # Process the frame data as needed
        results = frame_processing.process_frame(blob)
        emit('frame_response', results)
        
        print("Vide--------------------------------")
        print(results)
    except Exception as e:
        print(f"Error handling frame: {str(e)}")

  
recording = False
frames = []
audio_thread = None

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "audio.wav"

p = pyaudio.PyAudio()

def record_audio():
    global recording, frames
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()

def save_audio():
    global frames
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording, audio_thread
    if recording:
        return jsonify({"message": "Recording already in progress"}), 400
    recording = True
    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()
    return jsonify({"message": "Recording started"}), 200

TQandA={}
BQandA={}
@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recording, audio_thread, ans
    ques=request.json.get('ques')
    print(ques)
    if not recording:
        return jsonify({"message": "No recording in progress","answer":""}), 400
    recording = False
    audio_thread.join()
    save_audio()
    recognizer = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
        audio = recognizer.record(source)
    try:
        ans = recognizer.recognize_google(audio)
        print(ans)
        if chk:
            BQandA[ques]=ans
        else:
            TQandA[ques]=ans
        return jsonify({"message": "Recording stopped and transcribed", "answer": ans}), 200
    except sr.UnknownValueError:
        return jsonify({"message": "Google Speech Recognition could not understand audio","answer":""}), 400
    except sr.RequestError as e:
        return jsonify({"message": f"Could not request results from Google Speech Recognition service; {e}","answer":""}), 500
    
    
    

import pdf

@app.route('/analyse', methods=['GET'])
def analyse():
    global total_data
    global TQandA,BQandA,global_mail
    if len(TQandA)==0 and len(BQandA)==0:
        return jsonify({"message": "No questions or answers found"})
    
    print("*************Analyzing************")
    
    print(TQandA)
    print(BQandA)
    # chat model is now not available in free version
    project_score,project_rec = analysis.project_pre_analysis(total_data)
    TQandA = {'So, tell me about your "Finger Print Voting System using Web Development." How did you go about ensuring the security and accuracy of the fingerprint recognition system? \n': 'not use any security things in our project it was just the UI part we have designed so far so will be working on it later in the latest stages of our course', 'What specific UI elements or features did you prioritize in your design?': 'mostly I prayer I usually prefer HTML CSS in JavaScript and in some applications are usually use react JS', 'Interesting. Tell me about your approach to data visualization in your "Stock Prediction and Visualization" project. \n': 'so we actually to the date of from Wi-Fi and API and we have fine we are actually use the regression algorithm usually we actually use the regression algorithm to find the correlation between the data points and it gives a trend line for about 200 days for the future where it helps the investors to predict the future stocks and invest accordingly', "Let's start with a fundamental concept.  Can you explain what a data structure is, and give me an example of one you've used in a project? \n": 'so basically a data structure is a structure where we use the to store the data in the database and one of them is like the data structures which have learnt in the course workers stacks queues linked list and basically starts in involves last in first out the mechanism where the last element we have pushed into the stack will be the first one will be to be returned to the user', 'In your experience, what are the key differences between HTML and CSS?': 'HTML is a hypertext markup language and css is a cascading style sheet we use HTML to create a web page where as we use CSS towards styles to the web page and make it more visually attractive'}
    tech_score = analysis.technical_score(TQandA)
    BQandA = {"Let's say you're working on a complex project with a team, and you encounter a major obstacle. How do you approach the situation, and what steps would you take to overcome it? \n": 'well we actually find what are the issues with the project and will sort them out by by taking all the opinions within a team'}
    behavior_score = analysis.behavioral_score(BQandA)
    
    # print(project_score)
    print(tech_score)
    # print(behavior_score)    
    
    data=pdf.generate_pdf(tech_score,project_score,project_rec,behavior_score,"/Users/surya/Documents/MockInterviews/src/backend/newpdf.pdf")
    pdf.append_pdf_to_mongodb(global_mail,data)
    
    print("Data Updated ------------------------------")
    return jsonify({"project_score": tech_score})


app.route('/submit_answer', methods=['POST'])
def submit_answer():
    global prevQuestion, TQandA, BQandA
    
    answer=request.json.get('ans')
   
    
    print("***********************************")
    print(answer)

    if answer:
        # Save the answer (in-memory store or database)
        # Respond with a success message
        if prevQuestion in TQandA:
            TQandA[prevQuestion] = answer
        if prevQuestion in BQandA:
            BQandA[prevQuestion] = answer
            
        print(TQandA)
        print(BQandA)
        return jsonify({'message': 'Answer submitted successfully!'}), 200
    else:
        # Handle the case where no answer was provided
        return jsonify({'error': 'No answer provided!'}), 400
    
    
@app.route('/users', methods=['GET'])
def get_users():
    users = users_collection.find()
    user_data = [
        {
            "name": user['first_name'],
            "email": user['email'],
            "has_report": 'reports' in user  # Check if the user has a report
        } for user in users
    ]
    return jsonify(user_data)

from flask import Flask, send_file, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import io

@app.route('/report/<email>', methods=['GET'])
def get_report(email):
    user = users_collection.find_one({"email": email})
    print(user)
    if user and 'reports' in user:
        report_binary = user['reports'][0]
        return send_file(io.BytesIO(report_binary), download_name="report.pdf", as_attachment=True)
    else:
        return "Report not found", 404
    
    

# Endpoint to get all recruiters
@app.route('/recruiters', methods=['GET'])
def get_recruiters():
    recruiters = list(recruiter_collection.find())
    for recruiter in recruiters:
        recruiter['_id'] = str(recruiter['_id'])  # Convert ObjectId to string
    return jsonify(recruiters)

# Endpoint to delete a recruiter
@app.route('/recruiters/<id>', methods=['DELETE'])
def delete_recruiter(id):
    recruiter_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "Recruiter deleted"}), 200

# Endpoint to accept a recruiter and add to mail collection
@app.route('/recruiters/<id>/accept', methods=['POST'])
def accept_recruiter(id):
    recruiter = recruiter_collection.find_one({"_id": ObjectId(id)})
    if recruiter:
        main_recruiters_collection.insert_one(recruiter)  # Insert into mail_collection
        recruiter_collection.delete_one({"_id": ObjectId(id)})  # Remove from recruiters collection
        return jsonify({"msg": "Recruiter accepted"}), 200
    return jsonify({"msg": "Recruiter not found"}), 404

    
if __name__ == '__main__':
    socketio.run(app, debug=True)