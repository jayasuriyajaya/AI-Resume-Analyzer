import re


def check_section(
    text,
    keywords
):
    """
    Check whether a resume contains
    at least one keyword from a section.
    """

    text_lower = text.lower()

    return any(
        keyword.lower() in text_lower
        for keyword in keywords
    )


def check_contact_information(text):

    suggestions = []

    email_pattern = (
        r"[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    phone_pattern = (
        r"(\+?\d{1,3}[-.\s]?)?"
        r"\d{10}"
    )

    if not re.search(
        email_pattern,
        text
    ):

        suggestions.append({
            "priority": "High",
            "title": "Add an email address",
            "description": (
                "A professional email address "
                "helps recruiters contact you."
            )
        })

    if not re.search(
        phone_pattern,
        text
    ):

        suggestions.append({
            "priority": "High",
            "title": "Add a phone number",
            "description": (
                "Include a reachable phone number "
                "in your contact information."
            )
        })

    return suggestions


def check_resume_sections(text):

    suggestions = []

    sections = {

        "Professional Summary": [
            "summary",
            "profile",
            "objective"
        ],

        "Education": [
            "education",
            "academic",
            "qualification"
        ],

        "Experience": [
            "experience",
            "employment",
            "work history"
        ],

        "Projects": [
            "projects",
            "project experience"
        ],

        "Certifications": [
            "certification",
            "certifications"
        ]

    }

    for section, keywords in sections.items():

        if not check_section(
            text,
            keywords
        ):

            suggestions.append({

                "priority": (
                    "High"
                    if section
                    in [
                        "Professional Summary",
                        "Experience",
                        "Projects"
                    ]
                    else "Medium"
                ),

                "title": (
                    f"Add a {section} section"
                ),

                "description": (
                    f"Your resume does not appear "
                    f"to contain a clear {section} "
                    f"section."
                )

            })

    return suggestions


def check_achievements(text):

    suggestions = []

    achievement_patterns = [
        r"\d+%",
        r"\d+\+",
        r"\d+\s*users",
        r"\d+\s*projects",
        r"\d+\s*months",
        r"\d+\s*years",
        r"\d+\s*students",
        r"\d+\s*records"
    ]

    found = any(
        re.search(
            pattern,
            text,
            re.IGNORECASE
        )
        for pattern in achievement_patterns
    )

    if not found:

        suggestions.append({

            "priority": "Medium",

            "title": (
                "Add measurable achievements"
            ),

            "description": (
                "Use numbers, percentages, "
                "users, time saved, or other "
                "measurable results to demonstrate "
                "your impact."
            )

        })

    return suggestions


def generate_resume_suggestions(
    resume_text
):

    suggestions = []

    suggestions.extend(
        check_contact_information(
            resume_text
        )
    )

    suggestions.extend(
        check_resume_sections(
            resume_text
        )
    )

    suggestions.extend(
        check_achievements(
            resume_text
        )
    )

    return suggestions