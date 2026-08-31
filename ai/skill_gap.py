import re


def normalize_skill(skill):
    """
    Normalize a skill name for comparison.
    """

    return re.sub(
        r"[^a-z0-9+#.]",
        "",
        skill.lower()
    )


def parse_job_skills(skill_text):
    """
    Convert job skill text into a list.
    """

    if not skill_text:
        return []

    return [
        skill.strip()
        for skill in skill_text.split()
        if skill.strip()
    ]


def calculate_skill_gap(resume_skills, job_skill_text):
    """
    Compare resume skills against job requirements.
    """

    resume_skill_map = {
        normalize_skill(skill["name"]): skill["name"]
        for skill in resume_skills
    }

    job_skills = parse_job_skills(
        job_skill_text
    )

    matched_skills = []
    missing_skills = []

    for job_skill in job_skills:

        normalized = normalize_skill(
            job_skill
        )

        if normalized in resume_skill_map:

            matched_skills.append(
                resume_skill_map[normalized]
            )

        else:

            missing_skills.append(
                job_skill
            )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required": len(job_skills)
    }