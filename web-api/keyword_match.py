from extract_keywords_from_jd import extract_keywords_from_jd

def compare_keywords(jd, skills, resume_text):
    skill_keywords = [k.strip().lower() for k in skills.split(",") if k.strip()]
    jd_keywords = extract_keywords_from_jd(jd)

    combined_keywords = list(set(skill_keywords + jd_keywords))
    resume_lower = resume_text.lower()

    matched = [k for k in combined_keywords if k in resume_lower]
    missing = [k for k in combined_keywords if k not in resume_lower]

    score = int((len(matched) / len(combined_keywords)) * 100) if combined_keywords else 0

    return {
        "ats_score": score,
        "matched_keywords": matched,
        "missing_keywords": missing
    }
