from fpdf import FPDF
from datetime import datetime

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
    "Name": "Katepally Varshitha",
    "Email": "katepallyvarshitha24@gmail.com",
    "Contact": "8688018609",
    "Date": datetime.today().strftime('%Y-%m-%d')
}

# Body details
scores = {
    "Projects": {
        "Adaptability": "4.5",
        "Innovation": "4.25",
        "Scalability": "4.8",
        "Apt use of technology": "5",
        "Significance": "4.6",
    },
    "Technical": {
        "Accuracy": "4",
        "Explanation": "3.8",
        "Depth of understanding": "4.5",
        "Relevance to the task": "4.3",
        "Suggestions": "Technical Expertise : Should focus on deepening expertise in the specific technologies relevant to the role, such as Kafka, Pinecone, and OpenAI API. Further exploration of advanced database concepts, including optimization and scalability, would be beneficial."
    },
    "Cognitive": {
        "Communication": "3",
        "Team Work and Collaboration": "4",
        "Suggestions": """Communication Skills : Should work on refining communication skills to convey technical information in a clear, concise, and engaging manner. Practice presenting technical concepts to diYerent audiences and work on improving his overall presentation skills.
Experience & Portfolio : Building a portfolio of relevant projects and highlighting past experiences related to the job description would further strengthen his candidacy.."""
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
pdf.output('detailed_report.pdf')

print("PDF created successfully!")