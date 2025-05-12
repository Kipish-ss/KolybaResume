from ml_backend.api.services.model_service import get_embedding_model, get_keybert_model
from sqlalchemy.orm import Session
from ml_backend.api.db.models import Resume
from ml_backend.api.models.schemas import AdaptationResponse
from ml_backend.api.services.cleaning_service import clean_text, translate


def is_repeated_word(phrase: str) -> bool:
    words = phrase.lower().split()
    return len(words) > 1 and any(word == words[0] for word in words[1:])


def extract_keywords(text: str, top_n) -> list[str]:
    model = get_keybert_model()
    keywords = model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        use_mmr=True,
        diversity=0.7,
        top_n=top_n * 2
    )

    filtered_keywords = [keyword.lower() for keyword, _ in keywords if not is_repeated_word(keyword)][:top_n]
    return filtered_keywords


def get_keywords_score(db: Session, resume_id: int, vacancy_text: str, top_n=20) -> AdaptationResponse:
    resume = db.get(Resume, resume_id)
    if not resume:
        return []
    resume_keywords = set(extract_keywords(resume.CleanedText, top_n=top_n))
    vacancy_text = translate(vacancy_text)
    vacancy_cleaned_text = clean_text(vacancy_text)
    vacancy_keywords = set(extract_keywords(vacancy_cleaned_text, top_n=top_n))
    missing_keywords = list(vacancy_keywords - resume_keywords)
    score = keyword_similarity(resume_keywords, vacancy_keywords)

    return AdaptationResponse(score=score, missing_keywords=missing_keywords)


def keyword_similarity(resume_keywords, vacancy_keywords) -> int:
    resume_key_text = " ".join(resume_keywords)
    vacancy_key_text = " ".join(vacancy_keywords)
    model = get_embedding_model()
    resume_embedding = model.encode(resume_key_text)
    vacancy_embedding = model.encode(vacancy_key_text)

    similarity = model.similarity(resume_embedding, vacancy_embedding)[0][0]

    return int(similarity * 100)
