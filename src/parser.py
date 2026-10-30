
import fitz
from docx import Document
import re

SKILLS = [
    "python", "java", "sql", "mysql",
    "machine learning", "deep learning",
    "nlp", "pandas", "numpy",
    "scikit-learn", "tensorflow",
    "pytorch", "html", "css",
    "javascript", "react", "docker",
    "aws", "git", "spring boot"
]

def extract_text(file):
    file.seek(0)

    if file.name.lower().endswith(".pdf"):
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)

    elif file.name.lower().endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)

    return ""

def extract_skills(text):
    text = text.lower()
    return [
        skill for skill in SKILLS
        if re.search(
            r"(?<!\w)" + re.escape(skill) + r"(?!\w)",
            text
        )
    ]
