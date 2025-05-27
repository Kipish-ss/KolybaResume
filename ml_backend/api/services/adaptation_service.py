import json
from ml_backend.api.services.keyword_service import extract_keywords
from ml_backend.api.services.model_service import get_embedding_model
from ml_backend.api.db.models import Resume
from ml_backend.api.models.schemas import AdaptationResponse
from ml_backend.api.services.cleaning_service import clean_text, translate


def get_keywords_score(resume: Resume, vacancy_text: str, clean: bool) -> AdaptationResponse:
    if clean:
        vacancy_text = translate(vacancy_text)
        vacancy_text = clean_text(vacancy_text)

    resume_keywords = set(json.loads(resume.Keywords))
    vacancy_keywords, vacancy_skills = extract_keywords(vacancy_text, extract_skills=True)
    missing_keywords = list(vacancy_skills - resume_keywords)
    score = keyword_similarity(resume_keywords, vacancy_keywords)
    return AdaptationResponse(score=score, missing_keywords=missing_keywords)


def keyword_similarity(resume_keywords: set[str], vacancy_keywords: set[str]) -> int:
    resume_key_text = " ".join(resume_keywords)
    vacancy_key_text = " ".join(vacancy_keywords)
    model = get_embedding_model()
    resume_embedding = model.encode(resume_key_text)
    vacancy_embedding = model.encode(vacancy_key_text)

    similarity = model.similarity(resume_embedding, vacancy_embedding)[0][0]

    return int(similarity * 100)
