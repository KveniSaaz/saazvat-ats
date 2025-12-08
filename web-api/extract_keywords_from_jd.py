def extract_keywords_from_jd(jd_text):
    doc = nlp(jd_text)
    
    keywords = set()

    # Option 1: Use noun chunks (like "Python experience", "project management")
    for chunk in doc.noun_chunks:
        keywords.add(chunk.root.text.lower())

    # Option 2 (optional): Use named entities (ORG, TECH, GPE)
    for ent in doc.ents:
        keywords.add(ent.text.lower())

    return list(keywords)
