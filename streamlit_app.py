import streamlit as st
import PyPDF2

# Define JD keywords for comparison (example)
jd1 = {
    "skills": ["Python", "SQL", "Machine Learning", "Leadership"],
    "certifications": ["AWS Certified", "PMP"],
    "technologies": ["Docker", "Kubernetes"]
}

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.lower()

# Check if uploaded PDF is actually a resume
def is_resume(text):
    resume_keywords = ["experience", "skills", "projects", "education", "certifications", "technologies"]
    return any(word in text for word in resume_keywords)

# Compare resume against JD and return missing items
def get_missing_qualifications(resume_text, jd_keywords):
    missing = {}
    for category, items in jd_keywords.items():
        missing_items = [item for item in items if item.lower() not in resume_text]
        if missing_items:
            missing[category] = missing_items
    return missing

st.title("Resume Relevance Checker")

uploaded_file = st.file_uploader("Upload your PDF Resume", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    
    if not is_resume(resume_text):
        st.warning("Uploaded file does not appear to be a resume.")
    else:
        missing_items = get_missing_qualifications(resume_text, jd1)
        if missing_items:
            st.subheader("Missing Qualifications / Skills / Certificates:")
            for category, items in missing_items.items():
                st.write(f"**{category.capitalize()}:** {', '.join(items)}")
        else:
            st.success("Resume has all required qualifications!")
