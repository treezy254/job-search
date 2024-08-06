import os
import re
from collections import defaultdict, Counter
import PyPDF2
import docx
import spacy
from .ai import get_bert_embedding

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return " ".join([paragraph.text for paragraph in doc.paragraphs])

def parse_cv(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_extension.lower() == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please use PDF or DOCX.")

    doc = nlp(text)

    entities = defaultdict(list)
    for ent in doc.ents:
        entities[ent.label_].append(ent.text)

    skill_keywords = set(['python', 'java', 'c++', 'javascript', 'react', 'node.js', 'sql', 'machine learning', 'data analysis'])
    skills = [token.text for token in doc if token.text.lower() in skill_keywords]

    education = []
    edu_keywords = set(['bachelor', 'master', 'phd', 'degree', 'diploma'])
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in edu_keywords):
            education.append(sent.text.strip())

    experience = []
    exp_keywords = set(['work experience', 'professional experience', 'employment history'])
    exp_section = False
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in exp_keywords):
            exp_section = True
        elif exp_section and sent.text.strip():
            experience.append(sent.text.strip())
        elif exp_section and not sent.text.strip():
            exp_section = False

    cv_embedding = get_bert_embedding(text)

    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = Counter(words)
    common_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'])
    keywords = [word for word, freq in word_freq.most_common(20) if word not in common_words]

    cv_data = {
        'entities': dict(entities),
        'skills': skills,
        'education': education,
        'experience': experience,
        'keywords': keywords,
        'embedding': cv_embedding
    }

    return cv_data, text
