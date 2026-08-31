from pathlib import Path
from uuid import uuid4

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from werkzeug.utils import secure_filename

from database.db import get_db_connection
from ai.resume_parser import extract_resume_text
from ai.resume_analyzer import analyze_resume
from ai.job_recommender import recommend_jobs
from ai.skill_gap import calculate_skill_gap
from ai.learning_recommender import (
    recommend_learning_resources
)
from ai.career_score import (
    calculate_career_readiness
)

from ai.skill_coverage import (
    calculate_skill_coverage
)
from ai.readiness_status import (
    get_readiness_status
)
from ai.resume_improver import (
    generate_resume_suggestions
)
from ai.version_tracker import get_next_version


resume_bp = Blueprint("resume", __name__)


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"

ALLOWED_EXTENSIONS = {"pdf", "docx"}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@resume_bp.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        if "resume" not in request.files:
            flash("Please select a resume file.", "error")
            return redirect(url_for("resume.upload_resume"))

        file = request.files["resume"]

        if file.filename == "":
            flash("Please select a resume file.", "error")
            return redirect(url_for("resume.upload_resume"))

        if not allowed_file(file.filename):
            flash("Only PDF and DOCX files are allowed.", "error")
            return redirect(url_for("resume.upload_resume"))

        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_FILE_SIZE:
            flash("File size must be less than 5 MB.", "error")
            return redirect(url_for("resume.upload_resume"))

        original_filename = secure_filename(file.filename)

        unique_filename = (
            f"{uuid4().hex}_{original_filename}"
        )

        UPLOAD_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = UPLOAD_FOLDER / unique_filename

        file.save(file_path)
        try:

            extracted_text = extract_resume_text(file_path)

            analysis = analyze_resume(
                extracted_text
            )

        except Exception as error:

            file_path.unlink(missing_ok=True)

            flash(
                f"Could not process the resume: {error}",
                "error"
            )

            return redirect(
                url_for("resume.upload_resume")
            )

        connection = get_db_connection()

        cursor = connection.execute(
            """
            INSERT INTO resumes
            (user_id, filename, file_path, extracted_text)
            VALUES (?, ?, ?, ?)
            """,
            (
                session["user_id"],
                original_filename,
                str(file_path),
                extracted_text
            )
        )

        resume_id = cursor.lastrowid

        # --------------------------------------------------
# Save Resume Analysis
# --------------------------------------------------

        connection.execute(
            """
            INSERT INTO resume_analysis
            (resume_id, total_skills, resume_score, ats_score)
            VALUES (?, ?, ?, ?)
            """,
            (
                resume_id,
                analysis["total_skills"],
                analysis["resume_score"],
                analysis["ats_score"]
            )
        )

        # --------------------------------------------------
        # Save Resume Version
        # --------------------------------------------------

        version_number = get_next_version(
            connection,
            session["user_id"]
        )

        resume_row = connection.execute(
            """
            SELECT filename
            FROM resumes
            WHERE id = ?
            """,
            (resume_id,)
        ).fetchone()


        connection.execute(
            """
            INSERT INTO resume_versions (
                user_id,
                resume_id,
                version_number,
                filename,
                resume_score,
                ats_score,
                total_skills
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                resume_id,
                version_number,
                resume_row["filename"],
                analysis["resume_score"],
                analysis["ats_score"],
                analysis["total_skills"]
            )
        )


        for skill in analysis["skills"]:

            connection.execute(
                """
                INSERT OR IGNORE INTO skills
                (name, category)
                VALUES (?, ?)
                """,
                (
                    skill["name"],
                    skill["category"]
                )
            )

                    # --------------------------------------------------
        # Generate Job Recommendations
        # --------------------------------------------------
            resume_skill_names = [
                skill["name"]
                for skill in analysis["skills"]
            ]

            job_recommendations = recommend_jobs(
                resume_skill_names
            )


            skill_row = connection.execute(
                """
                SELECT id
                FROM skills
                WHERE name = ?
                """,
                (skill["name"],)
            ).fetchone()


            connection.execute(
                """
                INSERT OR IGNORE INTO resume_skills
                (resume_id, skill_id)
                VALUES (?, ?)
                """,
                (
                    resume_id,
                    skill_row["id"]
                )
            )


        connection.commit()
        connection.close()

        flash(
            "Resume uploaded successfully!",
            "success"
        )

        return redirect(
            url_for("resume.my_resumes")
        )


    return render_template("upload.html")


@resume_bp.route("/my-resumes")
def my_resumes():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    connection = get_db_connection()

    resumes = connection.execute(
        """
        SELECT *
        FROM resumes
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    return render_template(
        "my_resumes.html",
        resumes=resumes
    )


@resume_bp.route("/resume-analysis/<int:resume_id>")
def resume_analysis(resume_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    connection = get_db_connection()

    resume = connection.execute(
        """
        SELECT *
        FROM resumes
        WHERE id = ?
        AND user_id = ?
        """,
        (
            resume_id,
            session["user_id"]
        )
    ).fetchone()

    if not resume:
        connection.close()

        flash(
            "Resume not found.",
            "error"
        )

        return redirect(
            url_for("resume.my_resumes")
        )

    analysis_row = connection.execute(
        """
        SELECT *
        FROM resume_analysis
        WHERE resume_id = ?
        """,
        (resume_id,)
    ).fetchone()

    skills = connection.execute(
        """
        SELECT skills.name, skills.category
        FROM skills
        JOIN resume_skills
            ON skills.id = resume_skills.skill_id
        WHERE resume_skills.resume_id = ?
        ORDER BY skills.name
        """,
        (resume_id,)
    ).fetchall()

    connection.close()

    analysis = {
        "resume_score": analysis_row["resume_score"],
        "ats_score": analysis_row["ats_score"],
        "total_skills": analysis_row["total_skills"],
        "skills": skills
    }

    return render_template(
        "analysis.html",
        resume=resume,
        analysis=analysis
    )

@resume_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(
        url_for("auth.login")
    )

    connection = get_db_connection()


    resumes = connection.execute(
        """
        SELECT *
        FROM resumes
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        """,
        (session["user_id"],)
    ).fetchall()


    latest_resume = None
    latest_analysis = None
    recommendations = []
    resume_skills = []

    career_readiness = 0
    skill_coverage = 0
    best_job_match = 0
    readiness_status = "Not Analyzed"


    if resumes:

        latest_resume = resumes[0]


        latest_analysis = connection.execute(
            """
            SELECT *
            FROM resume_analysis
            WHERE resume_id = ?
            ORDER BY analyzed_at DESC
            LIMIT 1
            """,
            (latest_resume["id"],)
        ).fetchone()


        skill_rows = connection.execute(
            """
            SELECT skills.name
            FROM skills
            JOIN resume_skills
            ON skills.id = resume_skills.skill_id
            WHERE resume_skills.resume_id = ?
            """,
            (latest_resume["id"],)
        ).fetchall()

        resume_skills = [
            row["name"]
            for row in skill_rows
        ]


        connection.close()


        if latest_resume:

            recommendations = recommend_jobs(
                resume_skills,
                top_n=3
            )


            if recommendations:

                best_job = recommendations[0]
                best_job_match = float(
                    best_job.get(
                        "match_percentage",
                        0
                    )
                )

    required_skills = (
        list(
            best_job.get(
                "matched_skills",
                []
            )
        )
        +
        list(
            best_job.get(
                "missing_skills",
                []
            )
        )
    )

    skill_coverage = calculate_skill_coverage(
        resume_skills,
        required_skills
    )


    if latest_analysis:

        career_readiness = calculate_career_readiness(
            float(
                latest_analysis["resume_score"]
            ),
            float(
                latest_analysis["ats_score"]
            ),
            skill_coverage,
            best_job_match
        )

        readiness_status = get_readiness_status(
            career_readiness
        )


        return render_template(
            "dashboard.html",
            resumes=resumes,
            latest_resume=latest_resume,
            latest_analysis=latest_analysis,
            recommendations=recommendations,
            career_readiness=career_readiness,
            skill_coverage=skill_coverage,
            best_job_match=best_job_match,
            readiness_status=readiness_status
        )


@resume_bp.route(
    "/resume-improvements/<int:resume_id>"
)
def resume_improvements(resume_id):

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    connection = get_db_connection()

    resume = connection.execute(
        """
        SELECT *
        FROM resumes
        WHERE id = ?
        AND user_id = ?
        """,
        (
            resume_id,
            session["user_id"]
        )
    ).fetchone()

    connection.close()


    if not resume:

        flash(
            "Resume not found.",
            "error"
        )

        return redirect(
            url_for("resume.my_resumes")
        )


    suggestions = generate_resume_suggestions(
        resume["extracted_text"]
    )


    return render_template(
        "resume_improvements.html",
        resume=resume,
        suggestions=suggestions
    )

@resume_bp.route("/resume-history")
def resume_history():

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    connection = get_db_connection()


    versions = connection.execute(
        """
        SELECT *
        FROM resume_versions
        WHERE user_id = ?
        ORDER BY version_number DESC
        """,
        (session["user_id"],)
    ).fetchall()


    connection.close()


    return render_template(
        "resume_history.html",
        versions=versions
    )

@resume_bp.route("/resume-compare/<int:version1>/<int:version2>")
def resume_compare(version1, version2):

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    connection = get_db_connection()

    versions = connection.execute(
        """
        SELECT *
        FROM resume_versions
        WHERE id IN (?, ?)
        AND user_id = ?
        ORDER BY version_number
        """,
        (
            version1,
            version2,
            session["user_id"]
        )
    ).fetchall()

    if len(versions) != 2:

        connection.close()

        flash(
            "Resume versions not found.",
            "error"
        )

        return redirect(
            url_for("resume.resume_history")
        )

    old_version = versions[0]
    new_version = versions[1]


    # --------------------------------------------------
    # Get Skills - Old Version
    # --------------------------------------------------

    old_skills_rows = connection.execute(
        """
        SELECT skills.name
        FROM skills
        JOIN resume_skills
            ON skills.id = resume_skills.skill_id
        WHERE resume_skills.resume_id = ?
        ORDER BY skills.name
        """,
        (
            old_version["resume_id"],
        )
    ).fetchall()


    # --------------------------------------------------
    # Get Skills - New Version
    # --------------------------------------------------

    new_skills_rows = connection.execute(
        """
        SELECT skills.name
        FROM skills
        JOIN resume_skills
            ON skills.id = resume_skills.skill_id
        WHERE resume_skills.resume_id = ?
        ORDER BY skills.name
        """,
        (
            new_version["resume_id"],
        )
    ).fetchall()


    connection.close()


    # --------------------------------------------------
    # Convert Database Rows to Sets
    # --------------------------------------------------

    old_skills = set(
        row["name"]
        for row in old_skills_rows
    )

    new_skills = set(
        row["name"]
        for row in new_skills_rows
    )


    # --------------------------------------------------
    # Calculate Skill Changes
    # --------------------------------------------------

    skills_added = sorted(
        new_skills - old_skills
    )

    skills_removed = sorted(
        old_skills - new_skills
    )

    skills_retained = sorted(
        old_skills & new_skills
    )


    # --------------------------------------------------
    # Score Differences
    # --------------------------------------------------

    score_difference = (
        new_version["resume_score"]
        - old_version["resume_score"]
    )

    ats_difference = (
        new_version["ats_score"]
        - old_version["ats_score"]
    )

    skills_difference = (
        new_version["total_skills"]
        - old_version["total_skills"]
    )


    return render_template(
        "resume_compare.html",

        old_version=old_version,
        new_version=new_version,
        score_difference=score_difference,
        ats_difference=ats_difference,
        skills_difference=skills_difference,
        skills_added=skills_added,
        skills_removed=skills_removed,
        skills_retained=skills_retained
    )

@resume_bp.route("/job-recommendations/<int:resume_id>")
def job_recommendations(resume_id):

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )


    connection = get_db_connection()


    resume = connection.execute(
        """
        SELECT *
        FROM resumes
        WHERE id = ?
        AND user_id = ?
        """,
        (
            resume_id,
            session["user_id"]
        )
    ).fetchone()


    if not resume:


        connection.close()

        flash(
            "Resume not found.",
            "error"
        )

        return redirect(
            url_for("resume.my_resumes")
        )


    skill_rows = connection.execute(
        """
        SELECT skills.name
        FROM skills
        JOIN resume_skills
        ON skills.id = resume_skills.skill_id
        WHERE resume_skills.resume_id = ?
        """,
        (resume_id,)
    ).fetchall()


    connection.close()


    resume_skill_names = [
        row["name"]
        for row in skill_rows
    ]


    recommendations = recommend_jobs(
        resume_skill_names,
        top_n=10
    )


    for job in recommendations:

        missing_skills = job.get(
            "missing_skills",
            []
        )

    learning_resources = (
        recommend_learning_resources(
            missing_skills
        )
    )

    job["learning_resources"] = (
        learning_resources
    )


    return render_template(
        "job_recommendations.html",
        resume=resume,
        recommendations=recommendations
    )
