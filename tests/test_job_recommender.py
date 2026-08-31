from ai.job_recommender import recommend_jobs


sample_resume = """
Python developer with experience in Flask,
Django, MySQL, Pandas, NumPy and Machine Learning.

Developed web applications and machine learning
projects using Python.

Experience with Git, GitHub and SQL databases.
"""


jobs = recommend_jobs(
    sample_resume,
    top_n=5
)


print("\nRecommended Jobs")
print("=" * 70)


for _, job in jobs.iterrows():

    print(
        f"{job['title']} | "
        f"{job['company']} | "
        f"{job['location']} | "
        f"{job['match_score']:.2f}%"
    )