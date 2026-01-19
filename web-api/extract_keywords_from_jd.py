import spacy

nlp = spacy.load("en_core_web_sm")  

def extract_keywords_from_jd(jd_text):
    doc = nlp(jd_text)
    keywords = set()

    for chunk in doc.noun_chunks:
        keywords.add(chunk.root.text.lower())

    for ent in doc.ents:
        keywords.add(ent.text.lower())

    return list(keywords)
