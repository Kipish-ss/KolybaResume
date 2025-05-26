from transformers import Pipeline
from ml_backend.api.services.model_service import get_embedding_model, get_keybert_model, get_skills_model
from ml_backend.api.db.models import Resume
from ml_backend.api.models.schemas import AdaptationResponse
from ml_backend.api.services.cleaning_service import clean_text, translate


def create_overlapping_chunks(text: str, tokenizer, max_length: int = 510, overlap: int = 50) -> list[dict]:
    full_tokens = tokenizer.encode(text, add_special_tokens=False)
    total_tokens = len(full_tokens)
    effective_max_length = max_length - 2

    if total_tokens <= effective_max_length:
        return [{
            'chunk_id': 0,
            'text': text,
            'start_token': 0,
            'end_token': total_tokens
        }]

    chunks = []
    chunk_id = 0
    start_token = 0

    while start_token < total_tokens:
        end_token = min(start_token + effective_max_length, total_tokens)
        chunk_tokens = full_tokens[start_token:end_token]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)

        chunks.append({
            'chunk_id': chunk_id,
            'text': chunk_text,
            'start_token': start_token,
            'end_token': end_token
        })

        if end_token >= total_tokens:
            break

        start_token = end_token - overlap
        chunk_id += 1

    return chunks


def extract_skills_from_chunk(chunk_text: str, pipe: Pipeline) -> set[str]:
    results = pipe(chunk_text)
    skills = []
    current_skill_words = []
    prev_end = 0
    for result in results:
        entity = result.get('entity', '')
        word = result.get('word', '')
        start = result['start']
        end = result['end']

        if entity.startswith('B-SKILL') and result['score'] > 0.6:
            if current_skill_words:
                skill = ''.join(current_skill_words).replace('##', '').strip()
                if skill and len(skill) > 1:
                    skills.append(skill)
            current_skill_words = [word]

        elif entity.startswith('I-SKILL') and current_skill_words:
            word = word if start == prev_end else ' ' + word
            current_skill_words.append(word)

        else:
            if current_skill_words:
                skill = ''.join(current_skill_words).replace('##', '').strip()
                if skill and len(skill) > 1:
                    skills.append(skill)
                current_skill_words = []

        prev_end = end

    if current_skill_words:
        skill = ''.join(current_skill_words).replace('##', '').strip()
        if skill:
            skills.append(skill)

    skills = set([skill.lower() for skill in skills])

    return skills


def extract_skills_from_long_document(text: str, max_length: int = 510,
                                      overlap: int = 50) -> set[str]:
    tokenizer, pipe = get_skills_model()

    chunks = create_overlapping_chunks(text, tokenizer, max_length, overlap)
    all_skills = set()

    for chunk in chunks:
        chunk_skills = extract_skills_from_chunk(chunk['text'], pipe)
        all_skills = all_skills.union(chunk_skills)

    return all_skills


def is_repeated_word(phrase: str) -> bool:
    words = phrase.lower().split()
    return len(words) > 1 and all(word == words[0] for word in words)


def extract_keywords(text: str, top_n=100) -> set[str]:
    model = get_keybert_model()

    keywords = model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 1),
        stop_words='english',
        use_mmr=True,
        diversity=0.7,
        top_n=top_n
    )

    keywords_2 = model.extract_keywords(
        text,
        keyphrase_ngram_range=(2, 2),
        stop_words='english',
        use_mmr=True,
        diversity=0.7,
        top_n=top_n
    )

    filtered_keywords_1 = set([keyword.lower() for keyword, score in keywords if
                               not is_repeated_word(keyword)][:top_n])

    filtered_keywords_2 = set([keyword.lower() for keyword, score in keywords_2 if
                               not is_repeated_word(keyword)][:top_n])

    return filtered_keywords_1.union(filtered_keywords_2)


def extract_keywords_chunked(text: str, max_tokens: int = 400, overlap_tokens: int = 50) -> set[str]:
    tokenizer, _ = get_skills_model()
    tokens = tokenizer.encode(text, add_special_tokens=False)
    total_tokens = len(tokens)

    if total_tokens <= max_tokens:
        return extract_keywords(text)

    all_keywords = set()
    start = 0

    while start < total_tokens:
        end = min(start + max_tokens, total_tokens)
        chunk_tokens = tokens[start:end]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)

        keywords = extract_keywords(chunk_text)
        all_keywords = all_keywords.union(keywords)

        if end >= total_tokens:
            break
        start = end - overlap_tokens

    return all_keywords


def get_keywords_score(resume: Resume, vacancy_text: str, clean: bool) -> AdaptationResponse:
    resume_keywords = extract_keywords_chunked(resume.CleanedText)
    if clean:
        vacancy_text = translate(vacancy_text)
        vacancy_text = clean_text(vacancy_text)

    vacancy_keywords = extract_keywords_chunked(vacancy_text)
    vacancy_skills = extract_skills_from_long_document(vacancy_text)
    vacancy_skills = vacancy_skills.intersection(vacancy_keywords)
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
