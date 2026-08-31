from ai.resume_improver import (
    generate_resume_suggestions
)


sample_resume = """
John Doe

john@example.com

Python Developer

Skills:
Python, Flask, MySQL, Git

Education:
Bachelor of Computer Applications

Projects:
AI Resume Analyzer
"""


suggestions = generate_resume_suggestions(
    sample_resume
)


print(
    "\nAI Resume Improvement Suggestions"
)

print(
    "=" * 70
)


for suggestion in suggestions:

    print(
        f"[{suggestion['priority']}] "
        f"{suggestion['title']}"
    )

    print(
        suggestion["description"]
    )

    print(
        "-" * 70
    )