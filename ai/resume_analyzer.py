from ai.skill_extractor import extract_skills
from ai.ats_scorer import calculate_ats_score


def calculate_resume_score(text, skills):
    """
    Calculate the general resume score.
    """

    score = 0

    text_lower = text.lower()

    # Skills
    if len(skills) >= 5:
        score += 30

    elif len(skills) >= 3:
        score += 20

    elif len(skills) >= 1:
        score += 10

    # Contact information
    if "@" in text:
        score += 10

    # Resume sections
    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications"
    ]

    section_count = 0

    for section in sections:

        if section in text_lower:
            section_count += 1

    score += min(
        section_count * 10,
        50
    )

    return min(score, 100)


def analyze_resume(text):
    """
    Perform complete resume analysis.
    """

    skills = extract_skills(text)

    resume_score = calculate_resume_score(
        text,
        skills
    )

    ats_score = calculate_ats_score(
        text,
        skills
    )

    return {
        "skills": skills,
        "total_skills": len(skills),
        "resume_score": resume_score,
        "ats_score": ats_score
    }