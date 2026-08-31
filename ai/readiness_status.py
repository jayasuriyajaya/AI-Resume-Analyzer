def get_readiness_status(score):

    if score >= 85:

        return {
            "label": "Excellent",
            "message": (
                "Your profile is highly competitive "
                "for the analyzed job roles."
            )
        }

    elif score >= 70:

        return {
            "label": "Good",
            "message": (
                "Your profile is strong, but there "
                "are opportunities for improvement."
            )
        }

    elif score >= 50:

        return {
            "label": "Developing",
            "message": (
                "You have a foundation, but "
                "additional skills can improve "
                "your job opportunities."
            )
        }

    else:

        return {
            "label": "Needs Improvement",
            "message": (
                "Focus on improving your resume "
                "and developing relevant skills."
            )
        }