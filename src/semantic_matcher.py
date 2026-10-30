
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache
import re

@lru_cache(maxsize=1)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def split_text(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p.strip() for p in parts if len(p.strip()) >= 15]

def semantic_similarity(resume, job_description):
    if not resume.strip() or not job_description.strip():
        return 0.0

    model = load_model()

    resume_parts = split_text(resume)
    job_parts = split_text(job_description)

    if not resume_parts or not job_parts:
        return 0.0

    # Limit text for an efficient first prototype
    resume_parts = resume_parts[:100]
    job_parts = job_parts[:50]

    resume_vectors = model.encode(
        resume_parts,
        normalize_embeddings=True
    )

    job_vectors = model.encode(
        job_parts,
        normalize_embeddings=True
    )

    similarities = cosine_similarity(
        job_vectors, resume_vectors
    )

    # Best resume evidence for each job requirement
    best_matches = similarities.max(axis=1)

    score = float(best_matches.mean()) * 100

    return round(max(0, min(score, 100)), 2)
