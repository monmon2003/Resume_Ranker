import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
job description = {jd}
Create a resume which will be ideal for the given job description.
The resume should consist of the following sections:

Education

Skills

Experience

Create hypothetical names for university, add some graduation year for example: 2025
example output:

skills : python, c++, java, pytorch, HTML, machine learning, data structures
education: Btech in Electrical Engineering, ABC University, 2025
experience: ML engineer intern, software engineer

"""

def get_score(resume, keywords):
    text = [resume, keywords]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)
    match = cosine_similarity(count_matrix)[0][1]
    match = match*100
    match = round(match,2)
    return match



st.title("Resume Ranker")
st.text("Rank the resumes according to the job description.")
jd = st.text_area("Paste job description here")
uploaded_files = st.file_uploader("Upload your resume", type="pdf", accept_multiple_files=True, help="Upload resume.")

submit = st.button('Rank the resumes.')
response = get_gemini_response(input_prompt.format(jd=jd))

 
if submit:
    if uploaded_files:
        scores = []
        for uploaded_file in uploaded_files:
            resume = input_pdf_text(uploaded_file)
            score = get_score(resume,response)
            scores.append((uploaded_file.name, score))
        
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        st.subheader("Ranking of Resumes:")
        for rank, (filename, score) in enumerate(sorted_scores, start=1):
            st.write(f"{rank}. {filename} - Score: {score}")
