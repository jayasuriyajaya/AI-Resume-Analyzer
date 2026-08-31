from ai.job_database import JOB_DATABASE


def recommend_jobs(resume_skills, top_n=5):
    """
    Recommend job roles based on resume skills.

    Parameters:
        resume_skills: List of skills detected from the resume.
        top_n: Number of job recommendations to return.

    Returns:
        List of recommended jobs sorted by match percentage.
    """

    # Normalize resume skills

    resume_skills = {
        skill.lower().strip()
        for skill in resume_skills
        if skill
    }


    recommendations = []


    # Compare resume skills with every job

    for job_title, job_data in JOB_DATABASE.items():

        required_skills = {
            skill.lower().strip()
            for skill in job_data["skills"]
        }


        # Skills present in resume

        matched_skills = (
            resume_skills & required_skills
        )


        # Skills missing from resume

        missing_skills = (
            required_skills - resume_skills
        )


        # Prevent division by zero

        if not required_skills:
            continue


        # Calculate percentage

        match_percentage = (
            len(matched_skills)
            / len(required_skills)
        ) * 100


        recommendations.append({

            "job_title": job_title,

            "description": job_data[
                "description"
            ],

            "location": job_data[
                "location"
            ],

            "experience": job_data[
                "experience"
            ],

            "employment": job_data[
                "employment"
            ],

            "skills": job_data[
                "skills"
            ],

            "match_percentage":
                round(match_percentage, 1),

            "matched_skills":
                sorted(matched_skills),

            "missing_skills":
                sorted(missing_skills)

        })


    # Sort highest match first

    recommendations.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )


    # Return requested number

    return recommendations[:top_n]