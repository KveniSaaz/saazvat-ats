def compare_keywords(jd, skills, resume_text):
    jd_keywords = [k.strip().lower() for k in skills.split(",") if k.strip()] if skills else []

    resume_lower = resume_text.lower()

    matched = []
    missing = []

    for skill in jd_keywords:
        if skill in resume_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0

    return {
        "ats_score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "resume_text": resume_text
    }
