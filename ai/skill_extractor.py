import re

from ai.skills import get_all_skills


def extract_skills(text):
    """
    Extract known technical skills from resume text.
    """

    detected_skills = []

    text_lower = text.lower()

    for skill_data in get_all_skills():

        skill_name = skill_data["name"]

        pattern = r"(?<!\w)" + re.escape(
            skill_name.lower()
        ) + r"(?!\w)"

        if re.search(pattern, text_lower):

            detected_skills.append(skill_data)

    return detected_skills