import streamlit as st
import pdfplumber
import re

st.title("Resume Relevance App")

# Keywords to identify a resume
resume_keywords = ["experience", "education", "skills", "technologies", "projects", "certifications"]

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF resume", type="pdf")

if uploaded_file:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    # Check if it is likely a resume
    text_lower = text.lower()
    if any(keyword.lower() in text_lower for keyword in resume_keywords):
        
        # Job Descriptions (example)
        jd1 = "Axion Ray’s mission is..."
        jd2 = "Detailed Job Descriptions for Walk-In Drive..."
        
        # Relevance calculation
        def calc_relevance(resume, jd):
            resume_words = set(re.findall(r'\b\w+\b', resume.lower()))
            jd_words = set(re.findall(r'\b\w+\b', jd.lower()))
            matched = resume_words.intersection(jd_words)
            return round(len(matched)/len(jd_words)*100, 2) if jd_words else 0

        score1 = calc_relevance(text, jd1)
        score2 = calc_relevance(text, jd2)

        st.write(f"Relevance for JD1: {score1}%")
        st.write(f"Relevance for JD2: {score2}%")
        
    else:
        st.warning("The uploaded file does not appear to be a valid resume. Please upload a proper resume PDF.")
