
import json
from pathlib import Path
from io import BytesIO

import pandas as pd

from src.parser import extract_text
from src.matcher import calculate_similarity
from src.semantic_matcher import semantic_similarity
from src.evaluator import evaluate_ranking


# Evaluation dataset folder
folder = Path("data/evaluation")

with open(folder / "labels.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

job_description = dataset["job_description"]
labels = dataset["labels"]

results = []

# Analyze evaluation resumes
for path in sorted(folder.glob("*.docx")):
    print(f"Analyzing {path.name}...", flush=True)

    # BytesIO supports seek, tell, and seekable
    file = BytesIO(path.read_bytes())
    file.name = path.name

    resume_text = extract_text(file)

    if not resume_text.strip():
        print(f"Skipping empty resume: {path.name}")
        continue

    tfidf_score = calculate_similarity(
        resume_text,
        job_description
    )

    semantic_score = semantic_similarity(
        resume_text,
        job_description
    )

    results.append({
        "Candidate": path.stem,
        "Human Label": labels[path.stem],
        "TF-IDF": tfidf_score,
        "Sentence-BERT": semantic_score
    })

df = pd.DataFrame(results)

if df.empty:
    raise ValueError("No valid resumes found.")

print("\nMODEL EVALUATION RESULTS")

summary = []

for model in ["TF-IDF", "Sentence-BERT"]:
    ranked_ids = df.sort_values(
        by=model,
        ascending=False
    )["Candidate"].tolist()

    metrics = evaluate_ranking(
        ranked_ids,
        labels,
        k=3
    )

    summary.append({
        "Model": model,
        **metrics
    })

    print(f"\n{model} Ranking:")
    print(" > ".join(ranked_ids))

summary_df = pd.DataFrame(summary)

print("\nPerformance Comparison:")
print(summary_df.to_string(index=False))

summary_df.to_csv(
    folder / "evaluation_results.csv",
    index=False
)

df.to_csv(
    folder / "candidate_scores.csv",
    index=False
)

print("\nReports saved successfully!")
print("Location: data/evaluation/")
