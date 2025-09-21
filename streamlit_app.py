import streamlit as st
import pdfplumber
import re

st.title("Resume Relevance App")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF resume", type="pdf")
if uploaded_file:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Define Job Descriptions
    jd1 = "Axion Ray’s mission is to hire skilled Python developers with experience in web frameworks, data analysis, and cloud technologies."
    jd2 = "Looking for candidates with certifications, projects, and experience in Machine Learning, Python, and deployment."

    # Define resume keywords to validate
    resume_keywords = ['experience', 'skills', 'technologies', 'certifications', 'education', 'projects', 'achievements']

    # Check if PDF is a resume
    text_lower = text.lower()
    if not any(word in text_lower for word in resume_keywords):
        st.error("This does not appear to be a resume. Please upload a valid resume PDF.")
    else:
        # Relevance calculation function
        def calc_relevance(resume, jd):
            resume_words = set(re.findall(r'\b\w+\b', resume.lower()))
            jd_words = set(re.findall(r'\b\w+\b', jd.lower()))
            matched = resume_words.intersection(jd_words)
            missing = jd_words - resume_words
            score = round(len(matched) / len(jd_words) * 100, 2) if jd_words else 0
            return score, missing

        # Calculate for each JD
        score1, missing1 = calc_relevance(text, jd1)
        score2, missing2 = calc_relevance(text, jd2)

        st.write(f"**Relevance for JD1:** {score1}%")
        st.write(f"**Missing in Resume for JD1:** {', '.join(missing1) if missing1 else 'None'}")

        st.write(f"**Relevance for JD2:** {score2}%")
        st.write(f"**Missing in Resume for JD2:** {', '.join(missing2) if missing2 else 'None'}")
