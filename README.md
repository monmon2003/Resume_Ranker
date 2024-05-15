# Resume Ranker

This is a Streamlit application for ranking resumes based on their relevance to a provided job description.

## Installation 

1. Clone this repository:
  ```
  git clone https://github.com/monmon2003/Resume_Ranker.git
  ```
2. Download the required dependencies:
  ```
  pip install -r requirements.txt
  ```
3. Set up environment variables:

Create a .env file in the project root directory.
Add your Google API key to the .env file:
```
GOOGLE_API_KEY=your_api_key_here
```
## Usage
1. Run the Streamlit application:
    ```bash
    streamlit run app1.py
2. Input the job description text in the provided text area.

3. Upload the resumes in PDF format using the file uploader.

4. Click the "Rank the resumes" button to see the ranked list based on the percentage match with the job description.

## Deployment Instructions
The app can be deployed on streamlit by following these steps:

1. Create a Streamlit Cloud account at share.streamlit.io
2. Connect your GitHub account and add the repository
3. Fill out the app's information and click "Advanced settings..." to add the api key to the secrets field.
4. After saving the api key, click on deploy.
5. Visit the deployment URL to access the app 







