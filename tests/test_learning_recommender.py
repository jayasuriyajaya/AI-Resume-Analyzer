from ai.learning_recommender import (
    recommend_learning_resources
)


missing_skills = [
    "Docker",
    "AWS",
    "Django"
]


resources = recommend_learning_resources(
    missing_skills
)


print("\nRecommended Learning Resources")
print("=" * 70)


for resource in resources:

    print(
        f"{resource['skill']} | "
        f"{resource['title']} | "
        f"{resource['platform']} | "
        f"{resource['level']}"
    )

    print(
        f"URL: {resource['url']}"
    )

    print("-" * 70)