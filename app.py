import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import re

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

input_prompt = """

### As a skilled Application Tracking System (ATS) with advanced knowledge in technology, your role is to meticulously evaluate a candidate's resume based on the provided job description. 

### Your evaluation will involve analyzing the resume for relevant skills, experiences, and qualifications that align with the job requirements. Look for keywords and specific criteria outlined in the job description to determine the candidate's suitability for the position.

### Provide a detailed assessment of how well the resume matches the job requirements, highlighting strengths, weaknesses, and any potential areas of concern. Offer constructive feedback on how the candidate can enhance their resume to better align with the job description and improve their chances of securing the position.

### Your evaluation should be thorough, precise, and objective, ensuring that the most qualified candidates are accurately identified based on their resume content in relation to the job criteria.

### Remember to utilize your expertise in technology to conduct a comprehensive evaluation that optimizes the recruitment process for the hiring company. Your insights will play a crucial role in determining the candidate's compatibility with the job role.
resume={text}
jd={jd}

### Evaluation output:
Calculate the percentage of match between the resume and the job description. Give a number and some explation

### Example output:
The percentage of match between the resume and the provided job description is: 90
"""




def extract_percentage(response):
    match = re.search(r'\d+%', response)
    if match:
        percentage = match.group(0)
        score = int(percentage[:-1])  
        return score
    else:
        return 0  



st.title("Resume Ranker")
st.text("Rank the resumes according to the job description.")
jd = st.text_area("Paste job description here")
uploaded_files = st.file_uploader("Upload your resume", type="pdf", accept_multiple_files=True, help="Upload resume.")

submit = st.button('Rank the resumes.')
if submit:
    if uploaded_files:
        scores = []
        for uploaded_file in uploaded_files:
            text = input_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt.format(text=text, jd=jd))
            score = extract_percentage(response)
            scores.append((uploaded_file.name, score))
        
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        st.subheader("Ranking of Resumes:")
        for rank, (filename, score) in enumerate(sorted_scores, start=1):
            st.write(f"{rank}. {filename} - Score: {score}")
