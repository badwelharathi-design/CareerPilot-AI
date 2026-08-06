# =========================================================
# LEARNING RESOURCES
# =========================================================

LEARNING_RESOURCES = {

    "Python": [
        {
            "title": "Python Basics",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        },
        {
            "title": "Python Practice",
            "type": "Practice",
            "platform": "Coding Practice",
            "level": "Beginner"
        }
    ],

    "SQL": [
        {
            "title": "SQL Fundamentals",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        },
        {
            "title": "SQL Query Practice",
            "type": "Practice",
            "platform": "Coding Practice",
            "level": "Beginner"
        }
    ],

    "Machine Learning": [
        {
            "title": "Machine Learning Fundamentals",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Intermediate"
        }
    ],

    "Data Visualization": [
        {
            "title": "Data Visualization Fundamentals",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        }
    ],

    "Pandas": [
        {
            "title": "Pandas for Data Analysis",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        }
    ],

    "NumPy": [
        {
            "title": "NumPy Fundamentals",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        }
    ],

    "Statistics": [
        {
            "title": "Statistics for Data Science",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        }
    ],

    "Deep Learning": [
        {
            "title": "Deep Learning Fundamentals",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Intermediate"
        }
    ],

    "Java": [
        {
            "title": "Java Programming Fundamentals",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        }
    ],

    "HTML": [
        {
            "title": "HTML & Web Fundamentals",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        }
    ],

    "CSS": [
        {
            "title": "CSS Fundamentals",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        }
    ],

    "JavaScript": [
        {
            "title": "JavaScript Fundamentals",
            "type": "Course",
            "platform": "Online Learning",
            "level": "Beginner"
        }
    ]

}


def get_resources(skills):

    resources = []

    for skill in skills:

        if skill in LEARNING_RESOURCES:

            resources.extend(
                LEARNING_RESOURCES[skill]
            )

    return resources