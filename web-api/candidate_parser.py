import re
import spacy
import requests
from datetime import datetime
import dateutil.parser as date_parser
from geopy.geocoders import Nominatim

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Initialize Geocoder with a custom user agent

geolocator = Nominatim(user_agent="srms_ats_final")

geolocator = Nominatim(user_agent="britannica_validator_ats")

def fetch_city_master_list():
    try:
        response = requests.get("http://localhost:8081/api/locations", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Warning: Local Location API unreachable: {e}")
    return []

CITY_MASTER_LIST = fetch_city_master_list()

def validate_indian_location(raw_text):
    """Standardizes location and ensures it belongs to India via Geopy."""
    if not raw_text or len(raw_text) < 3:
        return None
    try:
        location = geolocator.geocode(f"{raw_text}, India", addressdetails=True, timeout=5)
        if location:
            address = location.raw.get('address', {})
            if address.get('country_code') == 'in':
                city = (address.get('city') or address.get('town') or 
                        address.get('district') or address.get('county') or 
                        address.get('state_district'))
                if city:
                    return f"{city.upper()}, INDIA"
    except:
        pass
    return None

def extract_full_address(text: str, doc, lines):
    edu_headers = ["education", "academic", "university", "college", "schooling", "qualification"]
    contact_keywords = ["address", "location", "native", "residence", "hometown", "present address"]
    
    # 1. Identify Header Section
    edu_start = len(lines)
    for i, line in enumerate(lines):
        if any(h in line.lower() for h in edu_headers):
            edu_start = i
            break
    header_lines = lines[:edu_start]
    header_text_combined = " ".join(header_lines)

    # --- PRIORITY A: KEYWORD SEARCH ---
    for line in header_lines:
        low_line = line.lower()
        if any(key in low_line for key in contact_keywords):
            raw_val = re.sub(r'(address|location|native|hometown|[:\-])', '', line, flags=re.IGNORECASE).strip()
            # Remove pincodes
            raw_val = re.split(r'[, \-]\d{6}', raw_val)[0] 
            validated = validate_indian_location(raw_val)
            if validated: return validated

    # --- PRIORITY B: NLP ENTITIES (Spacy) ---
    header_doc = nlp(header_text_combined)
    for ent in header_doc.ents:
        if ent.label_ in ["GPE", "LOC"] and ent.text.upper() not in ["INDIA", "IND"]:
            validated = validate_indian_location(ent.text)
            if validated: return validated

    # --- PRIORITY C: LOCAL API DATABASE MATCH (The "Not Found" Fix) ---
    # We search the header text for any city name present in your DB
    for item in CITY_MASTER_LIST:
        city_name = item.get('city')
        if city_name:
            # Use word boundaries \b to ensure exact word matches
            pattern = rf'\b{re.escape(city_name)}\b'
            if re.search(pattern, header_text_combined, re.IGNORECASE):
                return f"{city_name.upper()}, INDIA"

    return "NOT FOUND"


def extract_experience_years(text: str):
    """Calculates professional experience while strictly merging overlapping dates."""
    exp_headers = ["experience", "work history", "employment", "professional background", "work experience"]
    edu_headers = ["education", "academic", "university", "qualification", "schooling"]
    
    lines = text.split('\n')
    experience_text_blocks = []
    is_exp_section = False

    for line in lines:
        clean_line = line.lower().strip()
        if any(h in clean_line for h in exp_headers):
            is_exp_section = True
            continue
        if any(h in clean_line for h in edu_headers):
            is_exp_section = False
            continue
        if is_exp_section:
            experience_text_blocks.append(line)

    relevant_text = " ".join(experience_text_blocks)
    date_pattern = r'((?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.\/]?)?\b\d{2,4})\s?[\-\–\—to]+\s?((?:\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s\.\/]?)?\b\d{2,4}|Present|Current|Now)'
    
    matches = re.findall(date_pattern, relevant_text, re.IGNORECASE)
    
    ranges = []
    for start, end in matches:
        try:
            s_date = date_parser.parse(start, fuzzy=True)
            e_date = datetime.now() if any(word in end.lower() for word in ["present", "current", "now"]) else date_parser.parse(end, fuzzy=True)
            if s_date < e_date:
                ranges.append([s_date, e_date])
        except:
            continue

    if not ranges:
        return "Fresher"

    # Merge overlapping ranges to prevent inflated years (fixes the "13 years" bug)
    ranges.sort(key=lambda x: x[0])
    merged = []
    if ranges:
        curr_start, curr_end = ranges[0]
        for next_start, next_end in ranges[1:]:
            if next_start <= curr_end:
                curr_end = max(curr_end, next_end)
            else:
                merged.append((curr_start, curr_end))
                curr_start, curr_end = next_start, next_end
        merged.append((curr_start, curr_end))

    total_months = 0
    for start, end in merged:
        diff = (end.year - start.year) * 12 + (end.month - start.month)
        total_months += diff

    years = round(total_months / 12, 1)
    return f"{years} Years" if years > 0.5 else "Fresher"

def extract_candidate_details(text: str):
    doc = nlp(text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # 1. Email Extraction
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    email_id = email_match.group() if email_match else "N/A"
    
    # 2. Mobile Extraction
    mobile_match = re.search(r'(\+?\d{1,3}[\s-]?)?(\d{10})', text)
    mobile_no = mobile_match.group(2) if mobile_match else "N/A"

    # 3. Name Extraction (Top 3 lines)
    candidate_name = "Not Found"
    for line in lines[:3]:
        if "@" not in line and not any(char.isdigit() for char in line) and 1 < len(line.split()) <= 4:
            candidate_name = line
            break

    # 4. Location Extraction (City, Country)
    native_place = extract_full_address(text, doc, lines)

    return {
        "name": candidate_name.upper() if 'candidate_name' in locals() else "NOT FOUND",
        "emailId": email_id if 'email_id' in locals() else "N/A",
        "mobileNo": mobile_no if 'mobile_no' in locals() else "N/A",
        "nativePlace": native_place,
        "experience": extract_experience_years(text)
    }

def calculate_ats_score(jd_text: str, skills_text: str, resume_text: str):
    target_content = (jd_text + " " + skills_text).lower()
    jd_words = set(re.findall(r'\w+', target_content))
    resume_words = set(re.findall(r'\w+', resume_text.lower()))
    
    if not jd_words:
        return 0, [], []
    
    matched = list(jd_words.intersection(resume_words))
    missing = list(jd_words - resume_words)
    score = int((len(matched) / len(jd_words)) * 100)
    
    return score, matched, missing