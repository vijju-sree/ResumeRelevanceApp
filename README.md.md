# Resume Relevance App

## Problem Statement
This app calculates how relevant a candidate's resume is compared to fixed Job Descriptions (JDs) in PDF format. It helps recruiters and candidates quickly understand the match between resumes and job requirements.


## Technologies Used
- Python
- Flask
- pdfplumber

## How It Works
1. Upload a PDF resume.
2. Extract text from the resume using pdfplumber.
3. Compare the extracted text against predefined Job Description(s).
4. Calculate a relevance score based on matching keywords.
5. Display the relevance percentages on the result page.

## Installation & Usage
1. Open terminal or Anaconda Prompt.
2. Navigate to the project folder:
```
cd C:\Users\l\OneDrive\Desktop\resume-check
```
3. (Optional) Activate conda environment:
```
conda activate resumeapp
```
4. Install dependencies:
```
pip install -r requirements.txt
```
5. Run the app:
```
python app.py
```
6. Open browser at:
```
http://127.0.0.1:5000/
```
7. Upload a resume PDF to see relevance scores.

## License
MIT License

