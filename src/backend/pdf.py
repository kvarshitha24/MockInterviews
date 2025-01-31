# from io import BytesIO
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, TA_JUSTIFY
# import io
# import matplotlib.pyplot as plt
# from pymongo import MongoClient,errors

# uri = "mongodb+srv://katepallyvarshitha03:4WRAK6oVvvZI4bV8@cluster0.z4l6zvm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# global ans
# ans = ""

# try:
#     client = MongoClient(uri)
#     client.admin.command('ismaster')
#     print("Connected to the database successfully.")
# except errors.ConnectionFailure:
#     print("Failed to connect to the database.")


# db = client['MockInterviews']
# users_collection = db['UsersDetails']
# resume_collection = db['ResumeDetails']
# # Function to generate a bar graph for
# def generate_pdf(data, filepath):
#     # Create a PDF document in memory
#     buffer = BytesIO()
#     pdf = SimpleDocTemplate(buffer, pagesize=letter)
#     elements = []
#     styles = getSampleStyleSheet()
#     styles['Normal'].alignment = TA_JUSTIFY

#     # Add title
#     title = Paragraph("Technical Assessment Report", styles['Title'])
#     elements.append(title)
#     elements.append(Spacer(1, 12))

#     # Scores Section
#     score_data = [["Technical Accuracy", "Clarity of Explanation", "Depth of Understanding", "Relevance to the Task"],
#                   [f"{data['technical accuracy']}/5", f"{data['Clarity of Explanation']}/5", 
#                    f"{data['Depth of Understanding']}/5", f"{data['Relevance to the Task']}/5"]]
    
#     table = Table(score_data, colWidths=[130, 130, 130, 130])
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, -1), 10),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#     ]))
    
#     elements.append(table)
#     elements.append(Spacer(1, 12))

#     # Add Suggestions
#     suggestions_title = Paragraph("Suggestions:", styles['Heading2'])
#     elements.append(suggestions_title)
#     for idx, suggestion in enumerate(data['Suggestions']):
#         suggestion_text = Paragraph(f"{idx + 1}. {suggestion}", styles['Normal'])
#         elements.append(suggestion_text)
#         elements.append(Spacer(1, 6))

#     # Add Recommendations
#     recommendations_title = Paragraph("Recommendations:", styles['Heading2'])
#     elements.append(recommendations_title)
#     for idx, recommendation in enumerate(data['Recommendations']):
#         recommendation_text = Paragraph(f"{idx + 1}. {recommendation}", styles['Normal'])
#         elements.append(recommendation_text)
#         elements.append(Spacer(1, 6))

#     # Build PDF to in-memory buffer
#     pdf.build(elements)

#     # Save PDF to file
#     buffer.seek(0)
#     with open(filepath, 'wb') as file:
#         file.write(buffer.read())

#     # Return the binary data for further use
#     buffer.seek(0)
#     return buffer.getvalue()
# # Function to append PDF to MongoDB
# def append_pdf_to_mongodb(user_email, pdf_data):
#     # Convert PDF to binary data
#     pdf_binary = pdf_data

#     # Find the user by email and replace the 'reports' field with the new PDF
#     users_collection.update_one(
#         {'email': user_email},
#         {'$set': {'reports': [pdf_binary]}},
#         upsert=True
#     )
    
#     print("PDF added successfully")





from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_pdf(data, project_data, project_rec, behavior_data, filepath):
    # Create a PDF document in memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    styles['Normal'].alignment = TA_JUSTIFY

    # Add title
    title = Paragraph("Technical Assessment Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Technical Scores Section
    score_data = [["Technical Accuracy", "Clarity of Explanation", "Depth of Understanding", "Relevance to the Task"],
                  [f"{data['technical accuracy']}/5", f"{data['Clarity of Explanation']}/5", 
                   f"{data['Depth of Understanding']}/5", f"{data['Relevance to the Task']}/5"]]
    
    table = Table(score_data, colWidths=[130, 130, 130, 130])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Add Technical Suggestions
    suggestions_title = Paragraph("Technical Suggestions:", styles['Heading2'])
    elements.append(suggestions_title)
    for idx, suggestion in enumerate(data['Suggestions']):
        suggestion_text = Paragraph(f"{idx + 1}. {suggestion}", styles['Normal'])
        elements.append(suggestion_text)
        elements.append(Spacer(1, 6))

    # Add Technical Recommendations
    recommendations_title = Paragraph("Technical Recommendations:", styles['Heading2'])
    elements.append(recommendations_title)
    for idx, recommendation in enumerate(data['Recommendations']):
        recommendation_text = Paragraph(f"{idx + 1}. {recommendation}", styles['Normal'])
        elements.append(recommendation_text)
        elements.append(Spacer(1, 6))

    # Project Scores Section
    project_scores_title = Paragraph("Project Scores:", styles['Heading2'])
    elements.append(project_scores_title)
    project_score_data = [["Adaptability", "Innovation", "Scalability", "Apt use of Technology", "Significance"],
                          [f"{project_data['Adaptability']}/5", f"{project_data['Innovation']}/5", 
                           f"{project_data['Scalability']}/5", f"{project_data['Apt use of technology']}/5",
                           f"{project_data['Significance']}/5"]]
    
    project_table = Table(project_score_data, colWidths=[100, 100, 100, 100, 100])
    project_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    
    elements.append(project_table)
    elements.append(Spacer(1, 12))

    # Project Suggestions
    project_suggestions_title = Paragraph("Project Suggestions:", styles['Heading2'])
    elements.append(project_suggestions_title)
    for idx, suggestion in enumerate(project_rec['Suggestions']):
        suggestion_text = Paragraph(f"{idx + 1}. {suggestion}", styles['Normal'])
        elements.append(suggestion_text)
        elements.append(Spacer(1, 6))

    # Project Recommendations
    project_recommendations_title = Paragraph("Project Recommendations:", styles['Heading2'])
    elements.append(project_recommendations_title)
    for idx, recommendation in enumerate(project_rec['Recommendations']):
        recommendation_text = Paragraph(f"{idx + 1}. {recommendation}", styles['Normal'])
        elements.append(recommendation_text)
        elements.append(Spacer(1, 6))

    # Behavior Scores Section
    behavior_scores_title = Paragraph("Behavior Scores:", styles['Heading2'])
    elements.append(behavior_scores_title)
    behavior_score_data = [["Communication", "Clarity of Explanation", "Presentation"],
                           [f"{behavior_data['communication']}/5", f"{behavior_data['Clarity of Explanation']}/5", 
                            f"{behavior_data['presentation']}/5"]]
    
    behavior_table = Table(behavior_score_data, colWidths=[150, 150, 150])
    behavior_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    
    elements.append(behavior_table)
    elements.append(Spacer(1, 12))

    # Build PDF to in-memory buffer
    pdf.build(elements)

    # Save PDF to file
    buffer.seek(0)
    with open(filepath, 'wb') as file:
        file.write(buffer.read())

    # Return the binary data for further use
    buffer.seek(0)
    return buffer.getvalue()


# tech_score = {'technical accuracy': 1, 'Clarity of Explanation': 1, 'Depth of Understanding': 1, 'Relevance to the Task': 1, 'Suggestions': ['The answers are very vague and lack technical detail. Provide specific examples and code snippets to demonstrate understanding.', 'Focus on explaining the actual implementation details, not just high-level concepts.', 'Explain the data preprocessing techniques used for DDoS attack classification in more detail.', "Clarify how the OpenAI API interacts with MongoDB and Pinecone in the 'Database Interaction Platform with AI' project."], 'Recommendations': ['Gain a deeper understanding of the technologies involved and focus on providing more specific and informative answers.', 'Demonstrate your technical skills through concrete examples and code.', 'Practice explaining technical concepts clearly and concisely.']}
# proj_score = {'Adaptability': 3, 'Innovation': 4, 'Scalability': 4, 'Apt use of technology': 4, 'Significance': 3}
# proj_rec = {"Suggestions": ["Consider exploring advanced AI techniques for natural language processing, such as transformers and language models, to further enhance the database interaction platform.", "Investigate using distributed systems and cloud computing platforms for scaling the DDoS attack classification system to handle larger volumes of traffic.", "Explore implementing real-time feedback mechanisms and personalized learning modules to improve the Virtual Interview Assistant's effectiveness.", "Focus on building a user-friendly interface for the Virtual Interview Assistant to enhance accessibility and ease of use."], "Recommendations": ["Continue pursuing projects that leverage AI and data-driven approaches to solve real-world problems.", "Seek opportunities to collaborate with industry professionals and participate in relevant hackathons to gain practical experience.", "Focus on developing strong technical skills in areas like natural language processing, machine learning, and cloud computing.", "Explore opportunities to publish your work in academic journals or present at conferences to showcase your achievements and gain recognition."]}
# beh_score = {'communication': 3, 'Clarity of Explanation': 3, 'presentation': 3}
# path = "/Users/surya/Documents/MockInterviews/src/backend/newpdf.pdf"
# generate_pdf(tech_score,proj_score,proj_rec,beh_score,path)


tech_score = {'technical accuracy': 2, 'Clarity of Explanation': 2, 'Depth of Understanding': 1, 'Relevance to the Task': 3, 'Suggestions': ['The candidate needs to learn the basics of fingerprint recognition and security. They should research methods like minutiae-based matching, feature extraction, and encryption techniques.', 'The candidate needs to review their explanation of data structures. They should clarify the differences between stacks, queues, and linked lists, and provide concrete examples of their usage in code.'], 'Recommendations': ['The candidate should focus on improving their understanding of fundamental computer science concepts related to security, data structures, and algorithms. They can achieve this through online courses, tutorials, and practice projects.', 'The candidate should practice explaining their projects clearly and concisely, focusing on the technical details and demonstrating their understanding of the concepts involved.']}


