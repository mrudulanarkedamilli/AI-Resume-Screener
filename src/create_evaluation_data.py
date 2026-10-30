
import json
from pathlib import Path
from docx import Document

folder = Path("data/evaluation")
folder.mkdir(parents=True, exist_ok=True)

job = (
    "We need a Data Scientist with Python, SQL, "
    "machine learning, Pandas, Scikit-learn, "
    "statistics and predictive modeling experience."
)

samples = {
    "candidate_1": (
        3,
        "Developed machine learning predictive models "
        "using Python, SQL, Pandas, Scikit-learn and statistics."
    ),
    "candidate_2": (
        2,
        "Python data analyst experienced with SQL, "
        "Pandas, statistics and data visualization."
    ),
    "candidate_3": (
        0,
        "Graphic designer experienced in Photoshop, "
        "illustration, branding and visual design."
    ),
    "candidate_4": (
        1,
        "Java and React developer building web applications "
        "with MySQL and REST APIs."
    ),
    "candidate_5": (
        3,
        "Data scientist building predictive analytics systems "
        "with Python, machine learning, SQL, "
        "Scikit-learn and statistical modeling."
    ),
    "candidate_6": (
        0,
        "Content writer experienced in marketing, "
        "copywriting, editing and social media."
    )
}

labels = {}

for candidate_id, (relevance, content) in samples.items():
    doc = Document()
    doc.add_heading(candidate_id, 0)
    doc.add_paragraph(content)
    doc.save(folder / f"{candidate_id}.docx")
    labels[candidate_id] = relevance

with open(folder / "labels.json", "w") as f:
    json.dump(
        {"job_description": job, "labels": labels},
        f,
        indent=2
    )

print("Created 6 evaluation resumes and labels.")
