
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.preprocess import (
    clean_text,
    extract_advanced_skills
)

def calculate_similarity(resume, job_description):
    resume = clean_text(resume)
    job_description = clean_text(job_description)

    if not resume or not job_description:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        vectors = vectorizer.fit_transform([
            resume,
            job_description
        ])

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(float(similarity) * 100, 2)

    except ValueError:
        return 0.0


def compare_skills(resume, job_description):
    resume_skills = extract_advanced_skills(resume)
    job_skills = extract_advanced_skills(job_description)

    resume_set = {
        skill
        for skills in resume_skills.values()
        for skill in skills
    }

    job_set = {
        skill
        for skills in job_skills.values()
        for skill in skills
    }

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)

    coverage = (
        len(matched) / len(job_set) * 100
        if job_set else 0
    )

    return {
        "matched": matched,
        "missing": missing,
        "coverage": round(coverage, 2),
        "required_count": len(job_set)
    }
