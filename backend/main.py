
from io import BytesIO

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.parser import extract_text
from src.matcher import calculate_similarity, compare_skills
from src.semantic_matcher import semantic_similarity

app = FastAPI(
    title="AI Resume Screener API",
    description="Resume screening using NLP and Sentence-BERT",
    version="1.0.0"
)

# Allow local Streamlit development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Screener API is running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    filename = resume.filename or ""

    if not filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty"
        )

    try:
        # Limit uploaded file size to 5 MB
        content = await resume.read(5 * 1024 * 1024 + 1)

        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Resume exceeds 5 MB limit"
            )

        file = BytesIO(content)
        file.name = filename

        text = extract_text(file)

        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail="No readable text found in resume"
            )

        tfidf = calculate_similarity(
            text, job_description
        )

        semantic = semantic_similarity(
            text, job_description
        )

        skills = compare_skills(
            text, job_description
        )

        return {
            "filename": filename,
            "tfidf_similarity": tfidf,
            "semantic_similarity": semantic,
            "skill_coverage": (
                skills["coverage"]
                if skills["required_count"] else None
            ),
            "matched_skills": skills["matched"],
            "missing_skills": skills["missing"],
            "status": "success"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Resume analysis failed"
        )

    finally:
        await resume.close()
