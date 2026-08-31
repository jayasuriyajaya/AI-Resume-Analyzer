from ai.career_score import (
    calculate_career_readiness
)

from ai.skill_coverage import (
    calculate_skill_coverage
)


resume_score = 78
ats_score = 84
skill_coverage = 80
job_match = 92


readiness = calculate_career_readiness(
    resume_score,
    ats_score,
    skill_coverage,
    job_match
)


print(
    f"Career Readiness: {readiness}%"
)


resume_skills = [
    "Python",
    "Flask",
    "MySQL",
    "Git"
]


required_skills = [
    "Python",
    "Flask",
    "MySQL",
    "Git",
    "Docker"
]


coverage = calculate_skill_coverage(
    resume_skills,
    required_skills
)


print(
    f"Skill Coverage: {coverage}%"
)