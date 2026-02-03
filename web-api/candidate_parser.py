import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_candidate_details(text: str):
    doc = nlp(text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # 1. Extract Email
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    email_id = email_match.group() if email_match else "N/A"
    
    email_prefix = ""
    if email_id != "N/A":
        email_prefix = email_id.split('@')[0].lower().replace('.', '').replace('_', '')

    # 2. Name Extraction (Fixed: No early return)
    candidate_name = "Not Found"
    potential_names = {}

    # Check top lines first as a strong signal
    for line in lines[:3]:
        if "@" in line or any(char.isdigit() for char in line):
            continue
        if 1 < len(line.split()) <= 4:
            # We don't return here; we just set it as a high-probability candidate
            candidate_name = line
            break

    # If top lines didn't give a clear name, use NLP + Email scoring
    if candidate_name == "Not Found":
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                clean_name = re.sub(r'[^a-zA-Z\s]', '', ent.text).strip()
                if 1 < len(clean_name.split()) < 4:
                    score = 0
                    # Check against email prefix
                    simplified = clean_name.lower().replace(" ", "")
                    if email_prefix and (email_prefix in simplified or simplified in email_prefix):
                        score += 100
                    potential_names[clean_name] = score

        if potential_names:
            candidate_name = max(potential_names, key=potential_names.get)

    # 3. Mobile Number
    mobile_match = re.search(r'(\+?\d{1,3}[\s-]?)?(\d{10})', text)
    mobile_no = mobile_match.group(2) if mobile_match else "N/A"

    native_place = "Not Found"
    
    # Priority A: Use spaCy's GPE (Geo-Political Entity) to extract JUST the city name
    for ent in doc.ents:
        if ent.label_ == "GPE":
            # This will pick 'Chennai' even if the line is '9797454561 sarath@reallygreatsite.com Chennai'
            native_place = ent.text
            break

    # Priority B: If NLP fails, clean the line manually
    if native_place == "Not Found":
        location_keywords = ["address", "location", "native", "hometown", "chennai", "bangalore"]
        for line in lines:
            if any(key in line.lower() for key in location_keywords):
                # Remove common noise from the location line
                cleaned_line = line
                if email_id != "N/A":
                    cleaned_line = cleaned_line.replace(email_id, "")
                if mobile_no != "N/A":
                    cleaned_line = cleaned_line.replace(mobile_no, "")
                
                # Remove labels and punctuation
                cleaned_line = re.sub(r'(address|location|native|hometown|[:\-])', '', cleaned_line, flags=re.IGNORECASE)
                native_place = cleaned_line.strip()
                break

    return {
        "name": candidate_name,
        "emailId": email_id,
        "mobileNo": mobile_no,
        "nativePlace": native_place
    }

def calculate_ats_score(jd_text, skills_text, resume_text):
    target_content = (jd_text + " " + skills_text).lower()
    jd_words = set(re.findall(r'\w+', target_content))
    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    
    if not jd_words: return 0, [], []
    
    matched = list(jd_words.intersection(resume_words))
    missing = list(jd_words - resume_words)
    score = int((len(matched) / len(jd_words)) * 100) if jd_words else 0
    
    return score, matched, missing