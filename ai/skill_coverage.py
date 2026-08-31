def calculate_skill_coverage(
    resume_skills,
    required_skills
):
    """
    Calculate percentage of required job skills
    already present in the resume.
    """

    if not required_skills:
        return 0

    resume_set = {
        skill.lower().strip()
        for skill in resume_skills
    }

    required_set = {
        skill.lower().strip()
        for skill in required_skills
    }

    matched = resume_set.intersection(
        required_set
    )

    coverage = (
        len(matched)
        / len(required_set)
    ) * 100

    return round(
        coverage,
        2
    )