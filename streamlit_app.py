import streamlit as st
import pdfplumber
import re

st.title("Resume Relevance App")

# Resume validation keywords
resume_keywords = ["experience", "skills", "education", "projects", "certifications", "technologies"]

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF resume", type="pdf")
if uploaded_file:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Function to check if PDF is a resume
    def is_resume(text):
        text_lower = text.lower()
        matches = [word for word in resume_keywords if word in text_lower]
        return len(matches) > 0

    # Job Descriptions
    jd1 = "Axion Ray’s mission is to develop innovative software solutions..."
    jd2 = "Detailed Job Descriptions for Walk-In Drive includes Python, Flask, and team collaboration..."

    # Relevance calculation function
    def calc_relevance(resume, jd):
        resume_words = set(re.findall(r'\b\w+\b', resume.lower()))
        jd_words = set(re.findall(r'\b\w+\b', jd.lower()))
        matched = resume_words.intersection(jd_words)
        return round(len(matched) / len(jd_words) * 100, 2) if jd_words else 0

    # Only calculate relevance if PDF seems like a resume
    if is_resume(text):
        score1 = calc_relevance(text, jd1)
        score2 = calc_relevance(text, jd2)
        st.write(f"Relevance for JD1: {score1}%")
        st.write(f"Relevance for JD2: {score2}%")
    else:
        st.warning("Uploaded PDF does not appear to be a resume. Relevance cannot be calculated.")
