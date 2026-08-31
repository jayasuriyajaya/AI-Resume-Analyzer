from pathlib import Path

import pandas as pd
import re


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

LEARNING_DATASET = (
    BASE_DIR / "data" / "learning_resources.csv"
)


# ============================================================
# LOAD LEARNING RESOURCES
# ============================================================

def load_learning_resources():

    if not LEARNING_DATASET.exists():

        raise FileNotFoundError(
            f"Learning dataset not found: "
            f"{LEARNING_DATASET}"
        )

    return pd.read_csv(
        LEARNING_DATASET
    )


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):

    if skill is None:
        return ""

    skill = str(skill).lower().strip()

    # Replace common separators with spaces
    skill = skill.replace("-", " ")
    skill = skill.replace("_", " ")
    skill = skill.replace("/", " ")

    # Remove special characters
    skill = re.sub(
        r"[^a-z0-9+#.\s]",
        "",
        skill
    )

    # Remove extra spaces
    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    return skill.strip()


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    "ml": "machine learning",

    "machinelearning": "machine learning",

    "ai": "artificial intelligence",

    "dl": "deep learning",

    "deeplearning": "deep learning",

    "nlp": "nlp",

    "natural language processing": "nlp",

    "sklearn": "scikit-learn",

    "scikit learn": "scikit-learn",

    "scikit": "scikit-learn",

    "tf": "tensorflow",

    "pytorch": "pytorch",

    "nodejs": "node.js",

    "node js": "node.js",

    "javascript": "javascript",

    "js": "javascript",

    "postgres": "postgresql",

    "postgres sql": "postgresql",

    "powerbi": "power bi",

    "power-bi": "power bi",

}


# ============================================================
# CANONICAL SKILL
# ============================================================

def canonical_skill(skill):

    normalized = normalize_skill(
        skill
    )

    # Remove spaces temporarily
    compact = normalized.replace(
        " ",
        ""
    )

    if normalized in SKILL_ALIASES:

        return SKILL_ALIASES[
            normalized
        ]

    if compact in SKILL_ALIASES:

        return SKILL_ALIASES[
            compact
        ]

    return normalized


# ============================================================
# RECOMMEND LEARNING RESOURCES
# ============================================================

def recommend_learning_resources(
    missing_skills
):

    resources = load_learning_resources()

    recommendations = []

    # Prevent duplicate resources
    added_resources = set()


    # --------------------------------------------------------
    # Loop through missing skills
    # --------------------------------------------------------

    for missing_skill in missing_skills:

        missing_canonical = canonical_skill(
            missing_skill
        )


        # ----------------------------------------------------
        # Compare with learning dataset
        # ----------------------------------------------------

        for _, resource in resources.iterrows():

            resource_skill = resource.get(
                "skill",
                ""
            )

            resource_canonical = canonical_skill(
                resource_skill
            )


            # ------------------------------------------------
            # Exact canonical match
            # ------------------------------------------------

            if (
                missing_canonical
                == resource_canonical
            ):

                resource_id = str(
                    resource.get(
                        "resource_id",
                        ""
                    )
                )

                if resource_id not in added_resources:

                    recommendations.append(
                        resource.to_dict()
                    )

                    added_resources.add(
                        resource_id
                    )

                continue


            # ------------------------------------------------
            # Partial matching
            # ------------------------------------------------

            if (
                missing_canonical
                and resource_canonical
                and (
                    missing_canonical in resource_canonical
                    or
                    resource_canonical in missing_canonical
                )
            ):

                resource_id = str(
                    resource.get(
                        "resource_id",
                        ""
                    )
                )

                if resource_id not in added_resources:

                    recommendations.append(
                        resource.to_dict()
                    )

                    added_resources.add(
                        resource_id
                    )


    return recommendations