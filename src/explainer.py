
import re
from sentence_transformers import util
from src.semantic_matcher import load_model
from src.preprocess import extract_advanced_skills


def split_requirements(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+|;", text)
    return [
        p.strip(" -•\t")
        for p in parts
        if len(p.strip()) >= 8
    ]


def split_resume(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [
        p.strip()
        for p in parts
        if len(p.strip()) >= 8
    ]


def explain_matches(resume, job_description):
    requirements = split_requirements(job_description)[:40]
    resume_parts = split_resume(resume)[:150]

    if not requirements or not resume_parts:
        return []

    model = load_model()

    req_vectors = model.encode(
        requirements,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    resume_vectors = model.encode(
        resume_parts,
        convert_to_tensor=True,
        normalize_embeddings=True
    )

    scores = util.cos_sim(req_vectors, resume_vectors)

    results = []

    for i, requirement in enumerate(requirements):
        best_idx = int(scores[i].argmax().item())
        score = float(scores[i][best_idx].item())

        req_skills = extract_advanced_skills(requirement)
        evidence_skills = extract_advanced_skills(
            resume_parts[best_idx]
        )

        required = {
            s for group in req_skills.values() for s in group
        }
        supported = {
            s for group in evidence_skills.values() for s in group
        }

        if required and not required.issubset(supported):
            status = "Review needed"
        elif score >= 0.65:
            status = "Strong semantic evidence"
        elif score >= 0.40:
            status = "Possible semantic evidence"
        else:
            status = "Weak semantic evidence"

        results.append({
            "Requirement": requirement,
            "Resume Evidence": resume_parts[best_idx],
            "Similarity": round(max(0, score) * 100, 2),
            "Status": status
        })

    return results
