import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
<<<<<<< HEAD

=======
>>>>>>> 2b367298ce4ca7a1ceb58d1d39c021a5d86a928a

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
Given the following job description:

{jd}

Create an ideal resume for this job description. The resume should follow this exact format:

---

**Name:** [Your Name Here]
**Email:** [your.email@example.com]
**Phone:** [123-456-7890]
**LinkedIn:** [linkedin.com/in/yourprofile]

---

**Education:**
  
....

---

**Skills:**


---

**Experience:**

---

Ensure the resume is realistic and includes hypothetical names for universities and companies, appropriate job titles, and example durations. Maintain this structure and formatting for consistency.
"""

<<<<<<< HEAD
def preprocess_text(text):
    # Convert the text to lowercase
    text = text.lower()
    
    # Remove punctuation from the text
    text = re.sub('[^a-z]', ' ', text)
    
    # Remove numerical values from the text
    text = re.sub(r'\d+', '', text)
    
    # Remove extra whitespaces
    text = ' '.join(text.split())
    
    return text

=======
>>>>>>> 2b367298ce4ca7a1ceb58d1d39c021a5d86a928a
def get_score(resume, keywords):
    resume, keywords = preprocess_text(resume),preprocess_text(keywords)
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
<<<<<<< HEAD
        st.subheader(response)

=======
>>>>>>> 2b367298ce4ca7a1ceb58d1d39c021a5d86a928a
        st.subheader("Ranking of Resumes:")
        for rank, (filename, score) in enumerate(sorted_scores, start=1):
            st.write(f"{rank}. {filename} - Score: {score}")
