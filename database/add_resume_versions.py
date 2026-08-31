import sqlite3

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = (
    BASE_DIR / "database.db"
)


connection = sqlite3.connect(
    DATABASE_PATH
)


connection.execute(
    """
    CREATE TABLE IF NOT EXISTS resume_versions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        resume_id INTEGER NOT NULL,

        version_number INTEGER NOT NULL,

        filename TEXT NOT NULL,

        resume_score REAL DEFAULT 0,

        ats_score REAL DEFAULT 0,

        total_skills INTEGER DEFAULT 0,

        uploaded_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (user_id)
            REFERENCES users(id),

        FOREIGN KEY (resume_id)
            REFERENCES resumes(id)

    )
    """
)


connection.commit()

connection.close()


print(
    "resume_versions table created successfully!"
)