import streamlit as st
import pdfplumber
import re

st.title("Resume Relevance App with Missing Qualification Report")

# Upload PDF
uploaded_file = st.file_uploader("Upload your PDF resume", type="pdf")
if uploaded_file:
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Job Descriptions
    jd1 = "Experience in Python, Flask, SQL, teamwork, communication."
    jd2 = "Knowledge of Machine Learning, pandas, data visualization, certifications."

    # Function to calculate relevance and missing keywords
    def analyze_resume(resume, jd):
        resume_words = set(re.findall(r'\b\w+\b', resume.lower()))
        jd_words = set(re.findall(r'\b\w+\b', jd.lower()))
        matched = resume_words.intersection(jd_words)
        relevance = round(len(matched)/len(jd_words)*100, 2) if jd_words else 0
        missing = jd_words - matched
        return relevance, missing

    score1, missing1 = analyze_resume(text, jd1)
    score2, missing2 = analyze_resume(text, jd2)

    # Display results
    st.write(f"**JD1 Relevance:** {score1}%")
    if missing1:
        st.write("**Missing from Resume (JD1):**", ", ".join(missing1))
    else:
        st.write("All JD1 requirements are present in the resume ✅")

    st.write(f"**JD2 Relevance:** {score2}%")
    if missing2:
        st.write("**Missing from Resume (JD2):**", ", ".join(missing2))
    else:
        st.write("All JD2 requirements are present in the resume ✅")
