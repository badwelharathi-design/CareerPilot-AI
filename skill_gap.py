# Career skill requirements

CAREER_SKILLS = {

    "Data Scientist": [
        "python",
        "sql",
        "pandas",
        "statistics",
        "machine learning",
        "data visualization"
    ],

    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "statistics",
        "scikit-learn",
        "tensorflow",
        "deep learning"
    ],

    "AI Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "nlp"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "statistics",
        "data visualization"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "git"
    ],

    "Backend Developer": [
        "python",
        "flask",
        "django",
        "sql",
        "api",
        "git"
    ],

    "Software Developer": [
        "java",
        "python",
        "sql",
        "data structures",
        "algorithms",
        "git"
    ],

    "Cyber Security Analyst": [
        "networking",
        "linux",
        "cyber security",
        "python",
        "ethical hacking"
    ],

    "Cloud Engineer": [
        "python",
        "aws",
        "docker",
        "linux",
        "cloud computing",
        "networking"
    ],

    "Android Developer": [
        "java",
        "kotlin",
        "android",
        "firebase",
        "xml"
    ]

}


def analyze_skill_gap(
    student_skills,
    career
):

    student_skills = student_skills.lower()

    required_skills = CAREER_SKILLS.get(
        career,
        []
    )


    matched_skills = []

    missing_skills = []


    for skill in required_skills:

        if skill.lower() in student_skills:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)


    total = len(required_skills)


    if total > 0:

        readiness = (
            len(matched_skills)
            / total
        ) * 100

    else:

        readiness = 0


    return {

        "matched": matched_skills,

        "missing": missing_skills,

        "readiness": round(
            readiness,
            2
        )

    }