from pathlib import Path

from ai.resume_parser import extract_resume_text


UPLOAD_FOLDER = Path("uploads")


def test_resume_files():

    resume_files = list(UPLOAD_FOLDER.glob("*.pdf"))
    resume_files += list(UPLOAD_FOLDER.glob("*.docx"))

    if not resume_files:
        print("No PDF or DOCX resume found in uploads folder.")
        return

    for resume in resume_files:

        print("\n" + "=" * 60)
        print(f"Testing: {resume.name}")
        print("=" * 60)

        text = extract_resume_text(resume)

        print(f"Characters extracted: {len(text)}")

        print("\nFirst 1000 characters:")
        print(text[:1000])


if __name__ == "__main__":
    test_resume_files()