from flask import Flask, render_template, request
import pdfplumber
import re

app = Flask(__name__)

# ------------------------
# Extract text from PDF
# ------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ------------------------
# Check if PDF is a Resume
# ------------------------
def is_resume(text):
    keywords = ["education", "experience", "skills", "projects", "certifications", "objective"]
    text_lower = text.lower()
    for word in keywords:
        if word in text_lower:
            return True
    return False

# ------------------------
# Calculate Resume Relevance Score
# ------------------------
def calculate_relevance(resume_text, job_desc):
    resume_text = resume_text.lower()
    job_desc = job_desc.lower()

    # Extract keywords
    resume_words = set(re.findall(r'\b\w+\b', resume_text))
    jd_words = set(re.findall(r'\b\w+\b', job_desc))

    # Matching words
    matched_words = resume_words.intersection(jd_words)

    # Relevance %
    if len(jd_words) == 0:
        return 0
    score = (len(matched_words) / len(jd_words)) * 100
    return round(score, 2)

# ------------------------
# FIXED JOB DESCRIPTIONS
# ------------------------
jd1 = """
Axion Ray’s mission is to improve the quality and safety of engineered products - airplanes,
electric vehicles, and medical devices, by creating the world’s best proactive management platform,
powered by the latest advances in artificial intelligence.
We are looking for candidates with a Bachelor's degree in Mechanical/Automotive/Production/Manufacturing engineering,
at least one year of experience in a manufacturing company, and strong knowledge of Python (Pandas)/R,
data exploration, and data analysis.
"""

jd2 = """
Detailed Job Descriptions for Walk-In Drive:
1. Data Science Interns - Work on data engineering, visualization, and deep learning models (GenAI, NLP, CV).
   Required: Python, Pandas, Spark, Tableau/Power BI, ML/DL algorithms, SQL.
2. Data Engineer Intern - Build scalable data pipelines, write complex SQL, Python, Spark, Kafka, PySpark, C++.
   Required: Programming skills, SQL, Pandas, Numpy, Databricks knowledge.
Education: B.Tech/BE (2023 batch or earlier).
Location: Pune (Onsite).
"""

# ------------------------
# Routes
# ------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return "⚠️ No file uploaded!"

        resume_file = request.files['resume']

        # ✅ Check if file is PDF
        if not resume_file.filename.lower().endswith('.pdf'):
            return "❌ Only PDF files are supported! Please upload a PDF resume."

        # Extract Resume Text
        resume_text = extract_text_from_pdf(resume_file)

        # ✅ Check if the uploaded PDF is a resume
        if not is_resume(resume_text):
            return "❌ The uploaded PDF does not seem like a resume. Please upload a proper resume."

        # Calculate Relevance
        score_jd1 = calculate_relevance(resume_text, jd1)
        score_jd2 = calculate_relevance(resume_text, jd2)

        return render_template('result.html', score_jd1=score_jd1, score_jd2=score_jd2)

    return render_template('index.html')

# ------------------------
# Run App
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
