def calculate_career_readiness(
    resume_score,
    ats_score,
    skill_coverage,
    job_match
):
    """
    Calculate overall career readiness.

    All inputs should be between 0 and 100.
    """

    resume_score = max(
        0,
        min(100, resume_score)
    )

    ats_score = max(
        0,
        min(100, ats_score)
    )

    skill_coverage = max(
        0,
        min(100, skill_coverage)
    )

    job_match = max(
        0,
        min(100, job_match)
    )

    readiness = (
        resume_score * 0.25
        + ats_score * 0.25
        + skill_coverage * 0.25
        + job_match * 0.25
    )

    return round(
        readiness,
        2
    )