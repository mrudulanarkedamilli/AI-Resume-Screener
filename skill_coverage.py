
from src.preprocess import extract_advanced_skills


def get_skill_coverage(resume_text, job_description):
    resume_skills = extract_advanced_skills(resume_text)
    job_skills = extract_advanced_skills(job_description)

    def flatten(skills):
        if isinstance(skills, dict):
            result = set()
            for values in skills.values():
                if isinstance(values, (list, tuple, set)):
                    result.update(str(v).lower() for v in values)
            return result
        if isinstance(skills, (list, tuple, set)):
            return {str(v).lower() for v in skills}
        return set()

    resume_set = flatten(resume_skills)
    job_set = flatten(job_skills)

    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)

    coverage = (
        round(len(matched) / len(job_set) * 100, 2)
        if job_set else None
    )

    return {
        "skill_coverage": coverage,
        "matched_skills": matched,
        "missing_skills": missing
    }
