import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "dataset", "careers.csv")

data = pd.read_csv(CSV_PATH)


# Combine important information
data["combined"] = (
    data["skills"].fillna("") + " " +
    data["interests"].fillna("") + " " +
    data["education"].fillna("")
)


# Convert text into numerical vectors
vectorizer = TfidfVectorizer()

career_vectors = vectorizer.fit_transform(
    data["combined"]
)


def recommend_career(
    skills,
    interests,
    education
):

    student_profile = (
        str(skills) + " " +
        str(interests) + " " +
        str(education)
    )

    # Convert student profile
    student_vector = vectorizer.transform(
        [student_profile]
    )

    # Calculate similarity
    similarity_scores = cosine_similarity(
        student_vector,
        career_vectors
    )[0]

    # Get best matches
    top_indices = similarity_scores.argsort()[-3:][::-1]

    recommendations = []

    for index in top_indices:

        career = data.iloc[index]["career"]

        score = similarity_scores[index] * 100

        recommendations.append({
            "career": career,
            "score": round(score, 2)
        })

    return recommendations