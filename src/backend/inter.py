import PyPDF2
import io
import textract
from tkinter import Tk, filedialog
import time
from bson.binary import Binary
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
app = Flask(__name__)
CORS(app)
projects_data = []
top_projects= []
tech=[]
def extract_text_from_pdf(file_content):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def extract_text_from_docx(file_content):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file.flush()  # Flush to ensure the content is written
            
            # Extract text from the temporary file
            text = textract.process(temp_file.name)
        
        return text.decode('utf-8')  # Convert bytes to string
    except Exception as e:
        print("Error:", e)
        return None

def extract_text_from_txt(file_content):
    return file_content.decode('utf-8')

import google.generativeai as genai
gapi_key = 'AIzaSyA2vsEVR7to4-1aUzEcMuTlTXG5-UaJRII'
genai.configure(api_key=gapi_key)
interviewermodel = genai.GenerativeModel('gemini-1.5-flash')

model = genai.GenerativeModel('gemini-1.5-flash',
                                  generation_config={"response_mime_type":"application/json"})

chat=interviewermodel.start_chat(history=[])
chat.send_message("""pretend you are a interviewer and stay in character for each response. Follow this rules: 
                  1.Dont give answers to the questions.
                  2.Ask only 1 question at a time
                  3.Generate next question based on the previous answer
                  """)


def interviewer(prompt):
  response=chat.send_message(prompt)
  return response.text

def interview(prompt):
    response=model.generate_content(prompt)
    return response.text

json_data=""
def upload_file():
    global projects_data,title_des,resume_details,json_data,top_projects,name,tech
    if 'resume' not in request.files:
        return 'No file part'
    
    file = request.files['resume']
    
    if file.filename == '':
        return 'No selected file'
    
    data = file.read()
    print(file.filename)
    pdf_data = Binary(data)
   
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
    text=''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    
    prompt = text + "\n\n" + "from the above resume extract data using this json schema {'name': str,'mail id': str,'projects'=[{'title': str,'description':str}],'technical_skills':[str,str]}" 
    json_data=interview(prompt).strip()
    json_data=eval(json_data)
    if isinstance(json_data, list):
        json_data=json_data[0]
    print(json_data)
    projects_data = json_data['projects'] 
    tech = json_data['technical_skills']  
    name = json_data['name'] 
    return  json_data

def greet(name):
    global top_projects
    prompt="greet the candidate: "+name+" and mention you as a interviewX bot and tell candidate that you will be taking his interview and ask him to get ready aand feel free with emojis in 30 words."
    greeting=interviewer(prompt)
    prompt = str(projects_data) + "\nextract top 2 projects from the given project list. add domain to the json schema. If there are more than 1 projects in a specific domain {web development,artificial intelligence, machine learning etc...} pick the best one according to you.json schema = {projects:[{'title':str,'description':str}]}"
    top_projects = (interview(prompt))
    top_projects = eval(top_projects)
    if isinstance(top_projects, list):
        top_projects = top_projects[0]
    return greeting



start_time=time.time()
pc=0
f=1
fg=0
def project_inter(ans):
    global start_time,pc,f,fg
    if f==0:
        while time.time()-start_time < 120:
            project_next_que_audio=interviewer(ans)
            print(project_next_que_audio)
            print("audio ended")
            qprompttext=interview(project_next_que_audio+" extract only question from the given text into the format: {'question': str}")
            print(qprompttext)
            q = eval(qprompttext)
            if isinstance(q, list):
                q = q[0]
            print("text ended")
            # elig = "question:"+qprompttext+"\nanswer:"+ans+"\ndont support any wrong or irrevalant answer."+"\ngive only yes or no as output.Example:Yes"
            # chk=interview(elig)
            # if 'no' in chk.lower():
            #     break
            return q['question'],0
        f=1
        pc+=1
    if f:
        if pc==2:
            if not fg:
                fg=0
            return technique(ans)
        else:
            project=top_projects["projects"][pc]
            start_time = time.time()
            prompt = str(project)+" ask only 1 question from the given project, Include title of the project in the question. Dont mixup 2 questions into 1 question"
            projectqueaud=interviewer(prompt)
            f=0
            qprompttext = projectqueaud
            return projectqueaud,0
    
fgg=0
def technique(ans):
    global fg,tech,fgg,start_time
    if fg==0:
        start_time=time.time()
        prompt = "say to {name} that now you are going to test his technical skills"
        interviewer(prompt)
        prompt="Now your task is to interview {name} on their technical skills, remember not to ask more than 3 questions on a single skill and level of questions asked should be from easy to medium"
        interviewer(prompt)
        prompt=str(tech)+"ask a single basic level question based on the given technical skills."
        techq=interviewer(prompt)
        fg=1
        print(techq)
        return techq,0
    else:
        while time.time()-start_time < 120:
            next_q=interviewer(ans + "if the answer is irrevalant or wrong move to the other skill.ask only technical questions and dont give complete answers after the user gives answer.")
            print(next_q)
            #print("audio ended")
            qprompt=interview(next_q+" extract only question from the given text in this format: {'question': str }")
            #print(qprompt)
            #print("text ended")
            q = eval(qprompt)
            if isinstance(q, list):
                q = q[0]
            return q['question'],0
    if not fgg:
        fgg=0
    return behavioural(ans)

def behavioural(ans):
    global fgg,start_time
    if fgg==0:
        start_time = time.time()
        prompt = "say to {name} that now you are going to test his behavioural skills"
        interviewer(prompt)
        prompt="Now your task is to interview {name} on his behavioural skills"
        interviewer(prompt)
        prompt="ask a single question"
        q=interviewer(prompt)
        fgg=1
        return q,1
    else:
        while time.time()-start_time < 60:
            next_que=interviewer(ans)
            print(next_que)
            qprompt=interview(next_que+" extract only question from the given text")
            return qprompt,1
    return "end",1

def end():
    end=interviewer("tell to {name} that you have finished the interview")
    return end