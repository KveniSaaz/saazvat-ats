from extract_keywords_from_jd import extract_keywords_from_jd

def compare_keywords(jd, skills, resume_text):
    # Convert manual skills to list
    skill_keywords = [k.strip().lower() for k in skills.split(",") if k.strip()] if skills else []

    # Extract keywords from JD using spaCy
    jd_keywords = extract_keywords_from_jd(jd)

    # Combine both lists (remove duplicates using set)
    combined_keywords = list(set(skill_keywords + jd_keywords))

    resume_lower = resume_text.lower()

    matched = []
    missing = []

    # Compare combined keywords with resume
    for skill in combined_keywords:
        if skill in resume_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    # ATS score based on combined keywords
    score = int((len(matched) / len(combined_keywords)) * 100) if combined_keywords else 0

    return {
        "ats_score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "resume_text": resume_text,
        "jd_keywords": jd_keywords,
        "skill_keywords": skill_keywords,
        "combined_keywords": combined_keywords
    }
