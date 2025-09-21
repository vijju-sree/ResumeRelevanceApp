import streamlit as st
import PyPDF2
import docx2txt

# ---------- Resume Keywords ----------
RESUME_KEYWORDS = [
    "experience", "skills", "certifications", "education", "technologies",
    "projects", "leadership", "achievements"
]

# ---------- Hard-coded example for demo ----------
# In production, JD will be uploaded
JD_LIST = []

def parse_resume(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = docx2txt.process(file)
        return text
    else:
        return ""

def is_resume(text):
    text = text.lower()
    return any(kw in text for kw in RESUME_KEYWORDS)

def calc_relevance(resume_text, jd_text):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    
    matched = resume_words.intersection(jd_words)
    missing = jd_words - resume_words
    
    score = round(len(matched) / len(jd_words) * 100, 2) if jd_words else 0
    # Verdict based on score
    if score >= 75:
        verdict = "High"
    elif score >= 50:
        verdict = "Medium"
    else:
        verdict = "Low"
    
    return score, list(missing), verdict

# ---------- Streamlit App ----------
st.title("Placement Resume Relevance Checker")

st.header("Step 1: Upload Job Descriptions (JD)")
uploaded_jds = st.file_uploader("Upload JD PDFs or DOCX", type=["pdf", "docx"], accept_multiple_files=True)
if uploaded_jds:
    JD_LIST.clear()
    for jd_file in uploaded_jds:
        text = parse_resume(jd_file)
        if text:
            JD_LIST.append(text)
    st.success(f"{len(JD_LIST)} JD(s) uploaded successfully!")

st.header("Step 2: Upload Resume")
resume_file = st.file_uploader("Upload your resume PDF/DOCX", type=["pdf", "docx"])

if resume_file and JD_LIST:
    resume_text = parse_resume(resume_file)
    if is_resume(resume_text):
        st.success("✅ This is a resume")
        
        for idx, jd_text in enumerate(JD_LIST):
            st.subheader(f"JD {idx+1} Analysis")
            score, missing, verdict = calc_relevance(resume_text, jd_text)
            st.write(f"**Relevance Score:** {score}%")
            st.write(f"**Missing Qualifications/Skills:** {missing if missing else 'None'}")
            st.write(f"**Verdict:** {verdict}")
            
            # Suggestion
            if missing:
                st.info("Suggestion: Work on the missing skills/qualifications to improve relevance.")
    else:
        st.error("❌ This PDF/DOCX does not appear to be a resume")
