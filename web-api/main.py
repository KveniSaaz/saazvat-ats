from fastapi import FastAPI, UploadFile, Form
from extract_text import extract_resume_text
from keyword_match import compare_keywords
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Allow your Angular frontend to call the backend
origins = [
    "http://localhost:4200",   # Angular local
    
    "*"  # Allow all origins (not recommended in production)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze_resume(
    jd: str = Form(...),
    skills: str = Form(""),
    resume: UploadFile = None
):
    resume_text = extract_resume_text(resume)
    result = compare_keywords(jd, skills, resume_text)
    return result
