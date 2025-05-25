from ml_backend.api.services.model_service import get_embedding_model, get_keybert_model, get_vacancies_stopwords
from ml_backend.api.db.models import Resume
from ml_backend.api.models.schemas import AdaptationResponse
from ml_backend.api.services.cleaning_service import clean_text, translate
from nltk.corpus import stopwords


def is_repeated_word(phrase: str) -> bool:
    words = phrase.lower().split()
    return len(words) > 1 and all(word == words[0] for word in words)


def extract_keywords(text: str, top_n) -> list[str]:
    model = get_keybert_model()
    custom_vacancy_stopwords = get_vacancies_stopwords()
    nltk_words = set(stopwords.words("english"))
    combined_stopwords = nltk_words.union(custom_vacancy_stopwords)
    keywords = model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words=list(combined_stopwords),
        use_mmr=True,
        diversity=0.7,
        top_n=top_n
    )

    filtered_keywords = [keyword.lower() for keyword, score in keywords if
                         not is_repeated_word(keyword) and score > 0.2][:top_n]
    return filtered_keywords


def get_keywords_score(resume: Resume, vacancy_text: str, clean: bool, top_n=20) -> AdaptationResponse:
    resume_keywords = set(extract_keywords(resume.CleanedText, top_n=top_n))
    if clean:
        vacancy_text = translate(vacancy_text)
        vacancy_text = clean_text(vacancy_text)
    
    vacancy_keywords = set(extract_keywords(vacancy_text, top_n=top_n))
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
