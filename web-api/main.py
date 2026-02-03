from fastapi import FastAPI, UploadFile, Form, File
from typing import List
from extract_text import extract_resume_text
from fastapi.middleware.cors import CORSMiddleware
from candidate_parser import extract_candidate_details, calculate_ats_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
def analyze_resume_folder(
    jd: str = Form(...),
    skills: str = Form(""),
    resumes: List[UploadFile] = File(...)
):
    results = []

    for resume in resumes:
        # Step 1: Extract Text
        text = extract_resume_text(resume)
        
        if not text:
            continue

        # Step 2: Extract Personal Basic Details
        candidate_info = extract_candidate_details(text)

        # Step 3: Run ATS Scoring
        score, matched, missing = calculate_ats_score(jd, skills, text)

        # Step 4: Format for Frontend (Angular/PrimeNG)
        results.append({
            "filename": resume.filename,
            "candidate": candidate_info,
            "ats_score": score,
            "matched": matched[:15], # Show top 15 skills
            "missing": missing[:15]
        })

    return {"results": results}