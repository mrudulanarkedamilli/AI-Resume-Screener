
# AI-Powered Automated Resume Screener

An AI-powered recruitment assistance application that analyzes resumes, compares candidates with job descriptions, identifies matching and missing skills, and generates downloadable reports.

## Features

- User Login and Registration
- Professional Streamlit Dashboard
- PDF and DOCX Resume Parsing
- TF-IDF Resume Matching
- Sentence-BERT Semantic Similarity
- Multiple Resume Ranking
- Skill Coverage and Gap Analysis
- Model Evaluation Dashboard
- FastAPI Backend Integration
- Candidate Analytics and Charts
- PDF and CSV Report Generation
- Screening History using SQLite

## Technology Stack

- Frontend: Streamlit
- Backend: Python, FastAPI
- NLP: TF-IDF, Sentence-BERT
- Machine Learning: Scikit-learn, Sentence Transformers
- Data Analysis: Pandas, NumPy
- Visualization: Plotly
- Database: SQLite
- Document Processing: PyMuPDF, python-docx
- PDF Reports: ReportLab

## Project Structure

    AI-Resume-Screener/
    ├── app.py
    ├── auth.py
    ├── login_page.py
    ├── dashboard_style.py
    ├── candidate_analytics.py
    ├── pdf_report.py
    ├── screening_history.py
    ├── history_page.py
    ├── src/
    ├── backend/
    └── requirements.txt

## Installation

Clone the repository:

    git clone https://github.com/mrudulanarkedamilli/AI-Resume-Screener.git

Open the project folder:

    cd AI-Resume-Screener

Create a virtual environment:

    python -m venv venv

Activate it on Windows:

    .\venv\Scripts\Activate.ps1

Install dependencies:

    pip install -r requirements.txt

## Running the Application

Start the Streamlit frontend:

    python -m streamlit run app.py

Open:

    http://localhost:8501

Start the FastAPI backend in a second terminal:

    python -m uvicorn backend.main:app --reload --port 8000

FastAPI documentation:

    http://localhost:8000/docs

## How It Works

1. Recruiter logs in to the application.
2. Recruiter uploads resumes in PDF or DOCX format.
3. The system extracts text and technical skills.
4. TF-IDF and Sentence-BERT calculate resume-job similarity.
5. Candidates are ranked by matching scores.
6. Skill coverage and missing skills are displayed.
7. Recruiter downloads PDF or CSV reports.
8. Screening results can be saved and viewed later.

## Model Evaluation

The project evaluates ranking quality using:

- Precision@K
- Recall@K
- NDCG@K

Initial evaluation was performed on a small synthetic dataset. These results are not evidence of real-world hiring accuracy.

## Privacy and Responsible Use

This is an educational recruitment assistance tool. Automated matching scores measure text relevance and detected skills, not candidate suitability. Final hiring decisions require human review.

Do not upload real candidate resumes, personal data, database files, or credentials to public repositories.

## Future Improvements

- Role-based recruiter and administrator access
- Improved skill extraction using domain-specific NLP
- More extensive model evaluation
- Secure cloud deployment
- Advanced recruitment analytics

## Project Status

Core features tested locally. Docker deployment remains pending.

## Author

Developed as an academic AI/ML project.
