import re

import spacy


nlp = spacy.load("en_core_web_sm")


def clean_text(text):
    """
    Clean resume text before NLP processing.
    """

    text = text.replace("\x00", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def process_text(text):
    """
    Process resume text using spaCy.
    """

    cleaned_text = clean_text(text)

    document = nlp(cleaned_text)

    return document