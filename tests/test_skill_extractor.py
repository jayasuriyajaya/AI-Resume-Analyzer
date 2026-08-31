from ai.skill_extractor import extract_skills


sample_resume = """
I am a Python developer with experience in Flask,
Django, MySQL and JavaScript.

I have worked on Machine Learning projects using
Pandas, NumPy and Scikit-learn.

I use Git and GitHub for version control.
"""


skills = extract_skills(sample_resume)


print("\nDetected Skills:")
print("-" * 40)

for skill in skills:
    print(
        f"{skill['name']} → {skill['category']}"
    )