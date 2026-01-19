from fastapi import FastAPI, UploadFile, Form, File
from typing import List
from extract_text import extract_resume_text
from keyword_match import compare_keywords
from fastapi.middleware.cors import CORSMiddleware

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
        filename = resume.filename.lower()

        if filename.endswith(".pdf"):
            file_type = "PDF"
        elif filename.endswith(".docx"):
            file_type = "WORD"
        else:
            results.append({
                "filename": resume.filename,
                "error": "Unsupported file type"
            })
            continue

        text = extract_resume_text(resume)

        analysis = compare_keywords(jd, skills, text)

        results.append({
            "filename": resume.filename,
            "file_type": file_type,
            "ats_score": analysis["ats_score"],
            "matched": analysis["matched_keywords"],
            "missing": analysis["missing_keywords"]
        })

    return {"results": results}
