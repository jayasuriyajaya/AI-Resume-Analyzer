import re


def contains_section(text, section_names):
    """
    Check whether a resume contains one of the given sections.
    """

    text_lower = text.lower()

    for section in section_names:

        if re.search(
            r"\b" + re.escape(section.lower()) + r"\b",
            text_lower
        ):
            return True

    return False


def calculate_ats_score(text, skills):
    """
    Calculate an ATS-style resume score.
    Maximum score: 100.
    """

    text_lower = text.lower()

    score = 0

    # --------------------------------------------------
    # 1. Contact Information — 10 points
    # --------------------------------------------------

    email_found = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
    )

    phone_found = bool(
        re.search(
            r"(\+?\d[\d\s().-]{8,}\d)",
            text
        )
    )

    if email_found:
        score += 5

    if phone_found:
        score += 5

    # --------------------------------------------------
    # 2. Professional Summary — 10 points
    # --------------------------------------------------

    if contains_section(
        text,
        [
            "summary",
            "professional summary",
            "profile",
            "objective",
            "career objective"
        ]
    ):
        score += 10

    # --------------------------------------------------
    # 3. Skills — 20 points
    # --------------------------------------------------

    skill_count = len(skills)

    if skill_count >= 10:
        score += 20

    elif skill_count >= 7:
        score += 15

    elif skill_count >= 4:
        score += 10

    elif skill_count >= 1:
        score += 5

    # --------------------------------------------------
    # 4. Education — 15 points
    # --------------------------------------------------

    if contains_section(
        text,
        [
            "education",
            "academic background",
            "academic qualification"
        ]
    ):
        score += 15

    # --------------------------------------------------
    # 5. Experience — 15 points
    # --------------------------------------------------

    if contains_section(
        text,
        [
            "experience",
            "work experience",
            "professional experience",
            "employment"
        ]
    ):
        score += 15

    # --------------------------------------------------
    # 6. Projects — 10 points
    # --------------------------------------------------

    if contains_section(
        text,
        [
            "projects",
            "academic projects",
            "personal projects"
        ]
    ):
        score += 10

    # --------------------------------------------------
    # 7. Certifications — 5 points
    # --------------------------------------------------

    if contains_section(
        text,
        [
            "certifications",
            "certificates",
            "licenses"
        ]
    ):
        score += 5

    # --------------------------------------------------
    # 8. Keywords — 10 points
    # --------------------------------------------------

    keyword_groups = [
        "developed",
        "implemented",
        "designed",
        "managed",
        "analyzed",
        "created",
        "optimized",
        "responsible"
    ]

    keyword_count = sum(
        1 for keyword in keyword_groups
        if keyword in text_lower
    )

    if keyword_count >= 5:
        score += 10

    elif keyword_count >= 3:
        score += 7

    elif keyword_count >= 1:
        score += 4

    # --------------------------------------------------
    # 9. Resume Length — 5 points
    # --------------------------------------------------

    word_count = len(
        text.split()
    )

    if 300 <= word_count <= 1200:
        score += 5

    elif 150 <= word_count < 300:
        score += 3

    # --------------------------------------------------
    # Final score
    # --------------------------------------------------

    return min(score, 100)