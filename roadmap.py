# Personalized Learning Roadmap

LEARNING_RESOURCES = {

    "python": {
        "level": "Beginner",
        "duration": "2 Weeks",
        "topics": [
            "Python Basics",
            "Variables and Data Types",
            "Functions",
            "Lists and Dictionaries",
            "Object Oriented Programming"
        ]
    },

    "sql": {
        "level": "Beginner",
        "duration": "1 Week",
        "topics": [
            "SQL Basics",
            "SELECT Queries",
            "WHERE and ORDER BY",
            "GROUP BY",
            "JOINS"
        ]
    },

    "statistics": {
        "level": "Beginner",
        "duration": "2 Weeks",
        "topics": [
            "Mean and Median",
            "Probability",
            "Variance and Standard Deviation",
            "Correlation",
            "Hypothesis Testing"
        ]
    },

    "machine learning": {
        "level": "Intermediate",
        "duration": "3 Weeks",
        "topics": [
            "Machine Learning Basics",
            "Regression",
            "Classification",
            "Clustering",
            "Model Evaluation"
        ]
    },

    "data visualization": {
        "level": "Beginner",
        "duration": "1 Week",
        "topics": [
            "Matplotlib",
            "Charts and Graphs",
            "Data Visualization Principles",
            "Dashboard Creation"
        ]
    },

    "pandas": {
        "level": "Beginner",
        "duration": "1 Week",
        "topics": [
            "DataFrames",
            "Data Cleaning",
            "Filtering Data",
            "Grouping Data",
            "Data Analysis"
        ]
    },

    "power bi": {
        "level": "Beginner",
        "duration": "2 Weeks",
        "topics": [
            "Power BI Basics",
            "Data Import",
            "Data Cleaning",
            "Visualizations",
            "Dashboard Creation"
        ]
    },

    "html": {
        "level": "Beginner",
        "duration": "1 Week",
        "topics": [
            "HTML Basics",
            "Forms",
            "Tables",
            "Semantic HTML",
            "Web Page Structure"
        ]
    },

    "css": {
        "level": "Beginner",
        "duration": "1 Week",
        "topics": [
            "CSS Basics",
            "Selectors",
            "Flexbox",
            "Grid",
            "Responsive Design"
        ]
    },

    "javascript": {
        "level": "Beginner",
        "duration": "2 Weeks",
        "topics": [
            "JavaScript Basics",
            "Functions",
            "DOM",
            "Events",
            "API Basics"
        ]
    },

    "react": {
        "level": "Intermediate",
        "duration": "2 Weeks",
        "topics": [
            "React Basics",
            "Components",
            "Props",
            "State",
            "React Hooks"
        ]
    },

    "git": {
        "level": "Beginner",
        "duration": "3 Days",
        "topics": [
            "Git Basics",
            "Repositories",
            "Commit",
            "Push and Pull",
            "GitHub"
        ]
    },

    "tensorflow": {
        "level": "Intermediate",
        "duration": "2 Weeks",
        "topics": [
            "TensorFlow Basics",
            "Neural Networks",
            "Model Training",
            "Model Evaluation"
        ]
    },

    "deep learning": {
        "level": "Intermediate",
        "duration": "3 Weeks",
        "topics": [
            "Neural Networks",
            "CNN",
            "RNN",
            "Model Training",
            "Deep Learning Projects"
        ]
    },

    "aws": {
        "level": "Intermediate",
        "duration": "2 Weeks",
        "topics": [
            "Cloud Basics",
            "EC2",
            "S3",
            "IAM",
            "Cloud Deployment"
        ]
    },

    "docker": {
        "level": "Intermediate",
        "duration": "1 Week",
        "topics": [
            "Docker Basics",
            "Images",
            "Containers",
            "Dockerfile",
            "Docker Compose"
        ]
    }

}


def create_roadmap(missing_skills):

    roadmap = []

    for index, skill in enumerate(
        missing_skills,
        start=1
    ):

        skill_key = skill.lower()

        resource = LEARNING_RESOURCES.get(
            skill_key
        )

        if resource:

            roadmap.append({

                "step": index,

                "skill": skill.title(),

                "level": resource["level"],

                "duration": resource["duration"],

                "topics": resource["topics"]

            })

        else:

            roadmap.append({

                "step": index,

                "skill": skill.title(),

                "level": "Beginner",

                "duration": "1 Week",

                "topics": [
                    f"Learn {skill}",
                    f"Practice {skill}",
                    f"Build a small project using {skill}"
                ]

            })

    return roadmap