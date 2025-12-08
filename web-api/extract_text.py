import pdfplumber
import docx

def extract_resume_text(file):
    ext = file.filename.split(".")[-1].lower()

    if ext == "pdf":
        with pdfplumber.open(file.file) as pdf:
            return "".join([page.extract_text() for page in pdf.pages])

    elif ext == "docx":
        document = docx.Document(file.file)
        return "\n".join([para.text for para in document.paragraphs])
