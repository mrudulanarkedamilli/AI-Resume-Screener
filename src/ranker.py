
import pandas as pd

from src.parser import extract_text
from src.matcher import calculate_similarity, compare_skills
from src.semantic_matcher import semantic_similarity


def analyze_resumes(files, job_description):
    results = []

    for index, file in enumerate(files, start=1):
        try:
            text = extract_text(file)

            if not text.strip():
                continue

            tfidf = calculate_similarity(
                text, job_description
            )

            semantic = semantic_similarity(
                text, job_description
            )

            skills = compare_skills(
                text, job_description
            )

            results.append({
                "Resume ID": f"Resume {index}",
                "TF-IDF (%)": tfidf,
                "Semantic (%)": semantic,
                "Skill Coverage (%)": skills["coverage"]
                    if skills["required_count"] else None,
                "Matched Skills": ", ".join(skills["matched"]),
                "Skills Not Found": ", ".join(skills["missing"])
            })

        except Exception as error:
            raise RuntimeError(
                f"Could not analyze Resume {index}: {error}"
            ) from error

    df = pd.DataFrame(results)

    if not df.empty:
        df = df.sort_values(
            by=["Semantic (%)", "Skill Coverage (%)"],
            ascending=False,
            na_position="last"
        ).reset_index(drop=True)

    return df
