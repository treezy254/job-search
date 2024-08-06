from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
bert_model = AutoModel.from_pretrained("bert-base-uncased")
job_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
job_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")

def get_bert_embedding(text):
    inputs = bert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def ai_vet_job(job_description, user_query, cv_text=""):
    input_text = f"{user_query} {cv_text}"
    inputs = job_tokenizer(input_text, job_description, return_tensors="pt", truncation=True, padding=True, max_length=512)

    with torch.no_grad():
        outputs = job_model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    relevance_score = probs[0][1].item()

    return relevance_score

def calculate_cv_job_similarity(cv_data, job_description):
    cv_skills = set(cv_data['skills'])
    job_skills = set(re.findall(r'\b\w+\b', job_description.lower()))
    skill_similarity = len(cv_skills.intersection(job_skills)) / len(cv_skills.union(job_skills))

    job_embedding = get_bert_embedding(job_description)
    embedding_similarity = cosine_similarity([cv_data['embedding']], [job_embedding])[0][0]

    total_similarity = 0.5 * skill_similarity + 0.5 * embedding_similarity

    return total_similarity

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
