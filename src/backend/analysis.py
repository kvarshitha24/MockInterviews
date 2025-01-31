import google.generativeai as genai
from flask import jsonify
import PyPDF2
import io
import PIL
from fpdf import FPDF
from datetime import datetime

gapi_key = 'AIzaSyA2vsEVR7to4-1aUzEcMuTlTXG5-UaJRII'
genai.configure(api_key=gapi_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def interview(prompt):
    json_model = genai.GenerativeModel('gemini-1.5-flash',
                                  generation_config={"response_mime_type":"application/json"})
    response = json_model.generate_content(prompt)
    return response.text

project_scores = ""
final_report = ""

def project_pre_analysis(json_data):
    
    f_scores ={'Adaptability':0,
            'Innovation':0,
            'Scalability':0,
            'Apt use of technology':0,
            'Significance':0,}
    # print(json_data)
    for project_data in json_data['projects']:
        project_data = str(project_data)
        # print(project_data)
        pmodel = genai.GenerativeModel("gemini-1.5-flash")
        response = pmodel.generate_content("""rate the project from the data:"""+ project_data + """/n
        Adaptability(0-5):
        Innovation(0-5):
        Scalability(0-5):
        Apt use of technology(0-5):
        Significance(0-5):
        Adaptability (0-5):
        High (5): The project demonstrates a robust and flexible approach. It can readily adapt to significant changes in requirements, resources, or the project environment.
        Medium (3): The project can adjust to moderate changes with minimal disruption. It may require some replanning or resource reallocation.
        Low (1): The project struggles to adapt to changes. Delays or setbacks are likely when faced with unforeseen circumstances.

        Innovation (0-5):
        High (5): The project introduces entirely new ideas or significantly improves upon existing ones.rare in google search results.
        Medium (3): The project incorporates original elements or a fresh perspective on existing ideas.somewhat common in google search results.
        Low (1): The project relies heavily on established methods and offers minimal originality. common in google search results.

        Scalability (0-5):
        High (5): The project design allows for easy replication or expansion to a larger scale with minimal modifications. It has the potential for significant impact.
        Medium (3): The project can be adapted to a larger scale with some adjustments to resources, infrastructure, or processes.
        Low (1): The project is highly specific to its current context and would be difficult or impractical to scale effectively.

        Apt use of technology (0-5):
        High (5): The project leverages technology strategically to achieve its goals in a novel, efficient, and impactful way. It utilizes cutting-edge solutions or optimizes existing technologies.
        Medium (3): The project uses technology effectively to support its objectives. It may integrate existing tools or adopt new technologies that are well-suited to the task.
        Low (1): The project underutilizes technology or relies on outdated or inefficient solutions. Technology use hinders rather than enhances project goals.

        Significance(0-5):
        0: Not relevant or significant. The project does not address a real issue or problem within its field.
        1: Somewhat relevant. The project addresses a topic within the field, but its significance is limited.
        2: Moderately significant. The project addresses a relevant issue, but its potential contribution is not very clear.
        3: Significant. The project addresses a relevant issue or problem and has the potential to contribute new knowledge or understanding to the field.
        4: Highly significant. The project addresses a critical issue or problem within the field and has the potential to make a significant impact.
        5: Exceptionally significant. The project tackles a highly important issue and has the potential to break new ground or significantly advance the field.
        """,
        generation_config = genai.GenerationConfig(
        temperature=0,))
        # print(response.text)
        scores=interview("extract the scores from the data\n in json format {'Adaptability': int, 'Innovation': int, 'Scalability': int, 'Apt use of technology': int, 'Significance': int}"+response.text)
        scores = eval(scores)
        if isinstance(scores, list):
            scores=scores[0]
        for i in scores:
            f_scores[i] += int(scores[i])

    for i in f_scores:
        f_scores[i] = round(f_scores[i]/len(json_data['projects']))
    
    sug = interview(str(json_data['projects'])+"/n these are the projects done by the student. Given below the scores for the projects/n"+str(f_scores)+"generate suggestions and recommendations for the student in json format.{'Suggestions':[str,str..], 'Recommendations':[str,str..] '}")
    print(f_scores)
    print(sug)
    return f_scores, sug

# data={'name': 'Suryateja Chittiprolu', 'mail id': 'suryatejach04@gmail.com', 'projects': [{'title': 'Database Interaction Platform with AI', 'description': 'Integrated the OpenAI API with MongoDB and Pinecone vector databases, enabling AI-driven interactions.\nDeveloped a system for executing Read operations via natural language prompts, removing the necessity for SQL\nknowledge.\nEnhanced database accessibility and usability by facilitating interactions in plain English.'}, {'title': 'DDoS Attack Classification', 'description': 'Built a classification system to identify and categorize DDoS attacks in network traffic.\nConducted data preprocessing, addressed class imbalance, and engineered features to improve model accuracy.\nDeployed classification models, including Random Forest, SVM, and KNN, achieving high accuracy in differentiating\nbetween benign and malicious traffic.'}, {'title': 'Virtual Interview Assistant', 'description': 'Developed an AI-driven platform for generating dynamic interview questions and enabling real-time interaction\nbased on resume analysis.\nImplemented an animated avatar to simulate interview scenarios, enhancing engagement through synchronized\nspeech and actions.\nAutomated candidate assessment with AI models, significantly reducing manual review time and improving interview\ngrading precision.'}], 'technical_skills': ['Python', 'C', 'C++', 'SQL', 'MongoDB', 'KAFKA', 'Pinecone', 'HTML', 'CSS', 'ReactJS', 'Machine Learning', 'Large Language Models', 'GenerativeAI']}
# print(project_pre_analysis(data))
# project_pre_analysis(data)
import pdf
def technical_score(pro_tech):
    pro_tech=str(pro_tech)
    scores = interview(pro_tech + "\n" + "evaluate the above question and answers and rate the overall technical knowledge through parameters = ['technical accuracy',''Clarity of Explanation', 'Depth of Understanding', 'Relevance to the Task'], where each parameter should have a range of 0-5 and give recommendations in json format {'technical accuracy': score, 'Clarity of Explanation': score, 'Depth of Understanding': score, 'Relevance to the Task': score, 'Suggestions': [str,str....], 'Recommendations': [str,str....] }")
    scores = eval(scores)
    if isinstance(scores, list):
        scores=scores[0]
    return scores

# data={'technical accuracy': 1, 'Clarity of Explanation': 1, 'Depth of Understanding': 1, 'Relevance to the Task': 1, 'Suggestions': ['The answers are very vague and lack technical detail. Provide specific examples and code snippets to demonstrate understanding.', 'Focus on explaining the actual implementation details, not just high-level concepts.', 'Explain the data preprocessing techniques used for DDoS attack classification in more detail.', "Clarify how the OpenAI API interacts with MongoDB and Pinecone in the 'Database Interaction Platform with AI' project."], 'Recommendations': ['Gain a deeper understanding of the technologies involved and focus on providing more specific and informative answers.', 'Demonstrate your technical skills through concrete examples and code.', 'Practice explaining technical concepts clearly and concisely.']}
# score=technical_score(data)

# data=pdf.generate_pdf(score,r"/Users/surya/Documents/MockInterviews/src/backend/newpdf.pdf")
# pdf.append_pdf_to_mongodb('suryatejach04@gmail.com',data)
def behavioral_score(behavioural):
    scores = interview(str(behavioural)+"\n rate the overall candidate's behaviour with parameters like communication, clarity, presentation of facts with each parameter 0-5 and give recommendations in json format, where each parameter should have a range of 0-5 and give recommendations in json format {'communication': int, 'Clarity of Explanation': int, 'presentation': int }")
    scores = eval(scores)
    if isinstance(scores, list):
        scores=scores[0]
    return scores

class PDF(FPDF):
    def header(self):
        # Header details
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"Name: {header_details['Name']}", 0, 1, 'L')
        self.cell(0, 10, f"Email: {header_details['Email']}", 0, 1, 'L')
        self.cell(0, 10, f"Contact Number: {header_details['Contact']}", 0, 1, 'L')
        self.cell(0, 10, f"Date of Exam: {header_details['Date']}", 0, 1, 'L')
        self.ln(10)

    def footer(self):
        # Footer with website details
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Website: www.example.com | Contact: info@example.com', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

# Header details
header_details = {
    "Name": "jjjjj Doe",
    "Email": "johndoe@example.com",
    "Contact": "123-456-7890",
    "Date": datetime.today().strftime('%Y-%m-%d')
}

# Body details
scores = {
    "Projects": {
        "Adaptability": "Good",
        "Innovation": "Excellent",
        "Scalability": "Good",
        "Apt use of technology": "Very Good",
        "Significance": "High",
        "Suggestions": "Keep up the good work."
    },
    "Technical": {
        "Accuracy": "High",
        "Explanation": "Clear and Concise",
        "Suggestions": "Provide more examples."
    },
    "Cognitive": {
        "Communication": "Effective",
        "Suggestions": "Improve body language."
    }
}

# Create PDF object
pdf = PDF()

# Add a page
pdf.add_page()

# Add sections to the PDF
for section, details in scores.items():
    pdf.chapter_title(section)
    for key, value in details.items():
        pdf.chapter_body(f"{key}: {value}")

# Save the PDF to a file
# pdf.output('detailed_report.pdf')

# print("PDF created successfully!")

# final_report += scores +'\n'
# # report_data = project_data + "\n" + response.last + "\n"
# # scores = interview("extract scores from the data\n in json format {'Adaptability': int, 'Innovation': int, 'Scalability': int, 'Apt use of technology': int, 'Significance': int}"+response.last)
# # project_scores += scores + "\n"
# #     #print(scores.text)

# # project_score = interview(project_scores + "do the average of all scores for each parameter and return in the json format {'Adaptability': int, 'Innovation': int, 'Scalability': int, 'Apt use of technology': int,'Significance': int}")
# # final_report += project_scores+"\n"
# # # prompt_data = interview_data + "\n" + report_data + "\ngive 5-10 improvements and 5-10 recommendations from the given data, dont include any name just give points in the json format {'suggestions' = [str,str...] ,'recommendations'=[str,str...]}"
# # # suggestions = interview(prompt_data)
# # # print(suggestions)

# # # with open("/Users/SuryaTeja/Documents/project/report_data.txt", "w") as file:  
# # #     file.write(report_data+"\n\n\n\n")

behavioural = """
Question: Tell me about a time you had to work on a project where you needed to collaborate with a team of people who had different skill sets and perspectives. How did you ensure everyone felt heard and that you were working towards a shared goal?

Answer: At first, I would make a good conversation with all the people in the team to get to know their skill sets and perspectives. I would ensure that everyone in the team is comfortable sharing their thoughts. Later, we would discuss everyone’s perspectives and come to a conclusion with the best solutions. I believe working together towards a shared goal needs proper communication.

Question: Can you share one piece of advice you've learned about successful teamwork from your own experiences?

Answer: Yes, recently I worked on a project with my team members. My advice is to share everything that comes into your mind about the solution of the project, whether it is the correct one or not. If it is wrong, you can explore more about it. Nothing goes wrong. Everything has its own benefits.
"""
print(behavioral_score(behavioural))

# scores = interview(behavioural+"\n rate the overall candidate's behaviour with parameters like communication, clarity, presentation of facts with each parameter 0-5")
# final_report += scores + "\n"


# pro_tech = """
# Question: Can you elaborate on how you integrated the OpenAI API with MongoDB and Pinecone vector databases to enable those AI-powered interactions?

# Answer: Initially, we took dummy data of users from OpenAI by giving the prompt from the backend using its API. We then formatted that data into JSON and stored it in MongoDB using the insert_one function. Later, we converted the data into the form of embeddings and stored them in the Pinecone vector database.

# Question: Can you tell me more about the process of converting that data into embeddings for storage in Pinecone? What specific embedding model did you use, and what was the reasoning behind that choice?

# Answer: For comparing the data, embeddings are the best form. We used one of the models from ChatGPT to generate the embeddings for the given text. Embeddings are vector representations of the data, which in this case have around 1,523 dimensions. This high-dimensional representation allows us to compare and retrieve data very easily.

# Question: Can you elaborate on how you measured this performance improvement and what specific traditional databases you were comparing Kafka to?

# Answer: As we know, Kafka is a distributed platform. For example, if there are five sources and five targets each needing to transfer data from one source to all other targets, we would need 25 pipelines to transfer the data. However, with Kafka, we need only 10 such pipelines to transfer data from all sources to all other targets, which shows a clear performance improvement.

# Question: Can you explain how Kafka achieves this efficiency? How does it manage the routing and distribution of data to ensure it gets to all the intended targets?

# Answer: Kafka, being a distributed platform, stores data from all sources. When a target needs data from any source, it just requires one pipeline to get the data. Kafka stores the data in the form of topics, similar to how Oracle stores data in table format.

# Question: Imagine you're building a simple webpage to display product information from a database. Which of the technologies you've listed would be most directly involved in this task? And what would be the role of each one?

# Answer: To design a simple webpage to display product information dynamically, I would use ReactJS, CSS, Node.js, and MongoDB. ReactJS would be used for the frontend to display and retrieve information from the backend. CSS would be used to style the webpage. Node.js would be used to connect to MongoDB and write API calls. MongoDB would be used to store the data of the product.

# Question: Can you explain how Node.js would be used to connect to MongoDB and write API calls for retrieving product data?

# Answer: Using libraries in Node.js like mongoclient, we can connect to MongoDB and create the database as per our requirement. We can write GET API calls to retrieve the product data from the MongoDB collection.

# Question: Can you tell me more about how you'd structure those API calls for retrieving product data? Would you use a specific HTTP method like GET or POST? And what kind of data format would you typically send back to the ReactJS frontend?

# Answer: The structure is like userapp.get("path", (request, response) => {}). I would use the GET method to retrieve data, and I would send the data back in JSON format.

# Question: Can you explain how you would handle the situation if there was an error during the retrieval process from MongoDB? What steps would you take to ensure that the API call returns an appropriate response to the ReactJS frontend?

# Answer: Since almost all methods in MongoDB are asynchronous, I would use async and await methods. In Node.js, there is a method to handle errors in async functions. First, I would ensure that the given path and method are correct, then check for errors in the logic written."""

# prompt = pro_tech + "\n" + "evaluate the above question and answers and rate the overall technical knowledge through parameters = ['technical accuracy',''Clarity of Explanation', 'Depth of Understanding', 'Relevance to the Task'], where each parameter should have a range of 0-5 and give recommendations in json format {'technical accuracy': score, 'Clarity of Explanation': score, 'Depth of Understanding': score, 'Relevance to the Task': score, 'Suggestions': [str,str....], 'Recommendations': [str,str....] }"
# sc=(interview(prompt))
# final_report += sc

# print(final_report)

# with open('/Users/SuryaTeja/Documents/project/final_report.txt','w') as file:
#     file.write(final_report)