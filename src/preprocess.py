
import re

SKILL_CATEGORIES = {
    "Programming": {
        "Python": ["python"],
        "Java": ["java"],
        "JavaScript": ["javascript", "js"],
        "SQL": ["sql"],
    },
    "Data Science": {
        "Machine Learning": ["machine learning", "ml"],
        "Deep Learning": ["deep learning"],
        "NLP": ["nlp", "natural language processing"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Scikit-learn": ["scikit-learn", "sklearn"],
        "TensorFlow": ["tensorflow"],
        "PyTorch": ["pytorch"],
        "Statistics": ["statistics", "statistical analysis"],
    },
    "Web Development": {
        "HTML": ["html"],
        "CSS": ["css"],
        "React": ["react", "reactjs", "react.js"],
        "Spring Boot": ["spring boot"],
    },
    "Database": {
        "MySQL": ["mysql"],
        "PostgreSQL": ["postgresql", "postgres"],
        "MongoDB": ["mongodb"],
    },
    "Cloud & DevOps": {
        "Docker": ["docker"],
        "AWS": ["aws", "amazon web services"],
        "Git": ["git"],
        "Kubernetes": ["kubernetes", "k8s"],
        "Azure": ["azure"],
        "Google Cloud": ["google cloud", "gcp"],
    },
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_advanced_skills(text):
    text = clean_text(text)
    found = {}

    for category, skills in SKILL_CATEGORIES.items():
        matches = []

        for skill, aliases in skills.items():
            for alias in aliases:
                pattern = (
                    r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
                )
                if re.search(pattern, text):
                    matches.append(skill)
                    break

        if matches:
            found[category] = matches

    return found
