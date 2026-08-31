SKILL_DATABASE = {

    "programming_languages": [
        "Python",
        "Java",
        "C",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",
        "PHP",
        "Ruby",
        "Go",
        "Rust",
        "Kotlin",
        "Swift"
    ],

    "web_development": [
        "HTML",
        "CSS",
        "Bootstrap",
        "React",
        "Angular",
        "Vue",
        "Node.js",
        "Express.js",
        "Flask",
        "Django",
        "FastAPI"
    ],

    "databases": [
        "MySQL",
        "PostgreSQL",
        "SQLite",
        "MongoDB",
        "Oracle",
        "Redis",
        "Microsoft SQL Server"
    ],

    "data_science": [
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Keras",
        "Machine Learning",
        "Deep Learning",
        "Natural Language Processing",
        "NLP"
    ],

    "cloud_devops": [
        "AWS",
        "Microsoft Azure",
        "Google Cloud",
        "Docker",
        "Kubernetes",
        "Jenkins",
        "Git",
        "GitHub",
        "Linux"
    ],

    "tools": [
        "VS Code",
        "Jupyter",
        "Postman",
        "Figma"
    ]
}


def get_all_skills():
    """
    Return all skills with their categories.
    """

    skills = []

    for category, skill_list in SKILL_DATABASE.items():

        for skill in skill_list:

            skills.append({
                "name": skill,
                "category": category
            })

    return skills