def calculate_ats_score(
    semantic_score,
    matched_skills,
    missing_skills,
    experience_score,
    education_score
):
    """
    Calculate explainable ATS score.

    Weightage:
    Skill Match          = 40%
    Semantic Similarity  = 25%
    Experience Match     = 20%
    Education Match      = 15%
    """

    # -------------------------
    # Skill Match
    # -------------------------

    total_skills = (
        len(matched_skills)
        + len(missing_skills)
    )

    if total_skills > 0:
        skill_match_score = (
            len(matched_skills)
            / total_skills
        ) * 100
    else:
        skill_match_score = 0

    # -------------------------
    # Semantic Similarity
    # -------------------------

    semantic_score = float(semantic_score)

    # -------------------------
    # Experience
    # -------------------------

    experience_score = float(experience_score)

    # -------------------------
    # Education
    # -------------------------

    education_score = float(education_score)

    # -------------------------
    # Final ATS Score
    # -------------------------

    ats_score = (
        (skill_match_score * 0.40)
        +
        (semantic_score * 0.25)
        +
        (experience_score * 0.20)
        +
        (education_score * 0.15)
    )

    return round(ats_score, 2)