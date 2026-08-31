# 🤖 AI Resume Analyzer & Job Recommender

An AI-powered web application that analyzes resumes, evaluates ATS compatibility, identifies technical skills, detects skill gaps, recommends suitable career opportunities, and provides personalized resume improvement insights.

The project is designed to help students, job seekers, and professionals understand their resume quality and discover suitable career paths based on their existing skills.

---

## 📌 Project Overview

The **AI Resume Analyzer & Job Recommender** is a Flask-based career assistance platform that uses Natural Language Processing (NLP), Machine Learning techniques, and rule-based analysis to evaluate resumes.

Users can upload a resume and receive:

* Resume quality score
* ATS compatibility score
* Automatic skill extraction
* Skill gap analysis
* Job recommendations
* Job match percentage
* Career readiness score
* Resume improvement suggestions
* Resume history
* Resume version comparison
* Learning resource recommendations

---

# ✨ Features

## 📄 Resume Upload

Users can upload their resume through the web application.

The system extracts text from the uploaded resume and processes it for further analysis.

Supported resume processing includes PDF-based documents.

---

## 🧠 AI Resume Analysis

The application analyzes the extracted resume content and generates an overall resume score.

The analysis considers factors such as:

* Resume structure
* Skills
* Content quality
* Relevant information
* Resume completeness

---

## 📊 ATS Compatibility Score

The system provides an ATS-style compatibility score to help users understand how suitable their resume is for automated recruitment systems.

The score helps identify areas that may need improvement before applying for jobs.

---

## 🛠️ Automatic Skill Extraction

The application automatically identifies technical skills from resume content.

Detected skills can include technologies and tools such as:

* Python
* Java
* C++
* SQL
* HTML
* CSS
* JavaScript
* Flask
* Django
* Pandas
* NumPy
* Machine Learning
* Scikit-learn
* Git
* Power BI
* Excel

The skill database can be expanded as the project grows.

---

## 🎯 Job Recommendation Engine

The system compares the skills detected from a resume against predefined job requirements.

It calculates a job match percentage and ranks suitable career roles.

Example roles include:

* Python Developer
* Backend Developer
* Data Analyst
* Machine Learning Engineer
* Data Scientist
* Full Stack Developer
* Web Developer
* Software Developer

Each recommendation provides:

* Job title
* Job description
* Matching skills
* Missing skills
* Match percentage

---

## 🔍 Skill Gap Analysis

The application identifies the skills a user already possesses and the skills required for a selected career role.

This allows users to understand what they need to learn to become better qualified for their target role.

---

## 📚 Learning Recommendations

Based on identified skill gaps, the system can recommend learning resources to help users improve their technical skills.

---

## 📈 Career Readiness

The application calculates a career readiness score using multiple factors, including:

* Resume score
* ATS score
* Skill coverage
* Job match percentage

The system also provides a readiness status to help users understand their current career preparation level.

---

## ✏️ Resume Improvement

Users can receive suggestions for improving their resume content.

The improvement functionality helps identify areas that could be strengthened before submitting applications.

---

## 🕒 Resume History

The application stores uploaded resume versions so users can review their previous resumes and analyses.

---

## 🔄 Resume Comparison

Users can compare different resume versions to understand how their resume has changed.

The comparison functionality identifies:

* Skills added
* Skills removed
* Skills retained
* Differences between resume versions

---

# 🖥️ Application Pages

The application currently includes the following major pages:

| Page                | Purpose                              |
| ------------------- | ------------------------------------ |
| Home                | Introduces the AI Resume Analyzer    |
| Login               | User authentication                  |
| Register            | Create a new account                 |
| Dashboard           | Resume analytics and career overview |
| Upload Resume       | Upload and process resumes           |
| Resume Analysis     | Display resume and ATS analysis      |
| My Resumes          | View uploaded resumes                |
| Resume History      | View previous resume versions        |
| Resume Compare      | Compare resume versions              |
| Job Recommendations | View recommended career roles        |
| Resume Improvements | View resume improvement suggestions  |

---

# 🧰 Technologies Used

## Backend

* Python
* Flask
* SQLite

## AI / Machine Learning

* Scikit-learn
* NumPy
* Pandas
* NLTK
* Joblib

## Resume Processing

* PyPDF2
* NLP-based text processing

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* Bootstrap Icons

## Database

* SQLite

## Development Tools

* Visual Studio Code
* Python Virtual Environment
* Git / GitHub

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ Database Setup

The project uses SQLite.

The database is located at:

```text
database/database.db
```

If a new database needs to be created, run:

```bash
python database/init_db.py
```

The database contains tables for:

* Users
* Resumes
* Skills
* Resume Skills
* Resume Analysis
* Resume Versions

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key
```

Add any additional API keys required by your configuration.

**Never commit your `.env` file to GitHub.**

---

# ▶️ Running the Application

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Then run:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

# 🧪 Running Tests

The project includes automated tests for important components.

Run:

```bash
python -m pytest
```

If PyTest is not installed:

```bash
pip install pytest
```

Then run:

```bash
python -m pytest
```

---

# 🔄 Application Workflow

```text
User
 │
 ▼
Register / Login
 │
 ▼
Upload Resume
 │
 ▼
Resume Text Extraction
 │
 ▼
NLP Processing
 │
 ▼
Skill Extraction
 │
 ▼
Resume Analysis
 │
 ├── Resume Score
 ├── ATS Score
 └── Skills
 │
 ▼
Job Recommendation Engine
 │
 ├── Job Match
 ├── Matching Skills
 └── Missing Skills
 │
 ▼
Skill Gap Analysis
 │
 ▼
Learning Recommendations
 │
 ▼
Career Readiness
 │
 ▼
Resume Improvement
```

---

# 🗃️ Database Architecture

The main SQLite database contains the following tables:

### `users`

Stores registered user accounts.

### `resumes`

Stores uploaded resume information and extracted text.

### `skills`

Stores recognized technical skills.

### `resume_skills`

Connects resumes with their detected skills.

### `resume_analysis`

Stores resume analysis results.

### `resume_versions`

Stores resume version information used by the Resume History and Resume Comparison features.

---

# 🔒 Security Considerations

The project includes user authentication and user-specific resume access.

Important production improvements that can be added include:

* Password hashing
* CSRF protection
* File type validation
* File size limits
* Secure filename handling
* Production secret management
* Database backups
* Rate limiting

---

# 🚀 Future Enhancements

Potential future improvements include:

* Real-time job API integration
* LinkedIn job integration
* Indeed / job portal integrations
* Advanced AI-generated resume rewriting
* Cover letter generation
* Interview question generation
* AI interview practice
* Personalized learning paths
* Skill certification recommendations
* Resume templates
* Resume PDF generation
* Advanced analytics
* Admin dashboard
* Cloud deployment
* PostgreSQL support
* User profile management
* Email notifications
* Job application tracking

---

# 📸 Screenshots

Add screenshots of the application here.

Recommended screenshots:

1. Home Page
2. Login Page
3. Register Page
4. Dashboard
5. Resume Analysis
6. Job Recommendations
7. Skill Gap Analysis
8. Resume History
9. Resume Comparison
10. Resume Improvements

Example:

```markdown
## Dashboard

![Dashboard](static/images/dashboard.png)
```

---

# 🎓 Academic Project

This project can be used as an academic MCA project demonstrating practical implementation of:

* Web Development
* Python Programming
* Flask
* Database Management
* Natural Language Processing
* Machine Learning
* Resume Analysis
* Recommendation Systems
* Software Testing

---

# 👨‍💻 Author

**Jaya Suriya**

Master of Computer Applications (MCA)

---

# ⭐ Project Status

**Status: Active Development**

The core resume analysis, ATS scoring, skill extraction, job recommendation, career analytics, resume history, and resume comparison features are implemented and working.

More advanced AI-powered career features can be added in future versions.

---

## 📄 License

This project is intended for educational and portfolio purposes.
