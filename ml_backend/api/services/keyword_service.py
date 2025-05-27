from transformers import Pipeline, BertTokenizer
from ml_backend.api.services.model_service import get_keybert_model, get_skills_model


def create_overlapping_chunks(text: str, tokenizer: BertTokenizer, max_length: int = 512, overlap: int = 50) -> list[
    str]:
    full_tokens = tokenizer.encode(text, add_special_tokens=False, truncation=False)
    total_tokens = len(full_tokens)
    effective_max_length = max_length - 2

    if total_tokens <= effective_max_length:
        return [text]

    chunks = []
    start_token = 0

    while start_token < total_tokens:
        end_token = min(start_token + effective_max_length, total_tokens)
        chunk_tokens = full_tokens[start_token:end_token]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)

        if end_token >= total_tokens:
            break

        start_token = end_token - overlap

    return chunks


def extract_chunk_skills(chunk_text: str, pipe: Pipeline) -> set[str]:
    results = pipe(chunk_text)
    skills = []
    current_skill_words = []
    prev_end = 0
    for result in results:
        entity = result['entity']
        word = result['word']
        start = result['start']
        end = result['end']

        if entity.startswith('B-SKILL') and result['score'] > 0.6:
            if current_skill_words:
                skill = ''.join(current_skill_words).replace('##', '')
                skill = skill.strip()
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


def is_repeated_word(phrase: str) -> bool:
    words = phrase.lower().split()
    return len(words) > 1 and all(word == words[0] for word in words)


def extract_keywords(text: str, extract_skills: bool = False, top_n: int = 100, max_tokens: int = 510,
                     overlap_tokens: int = 50) -> set[str] | tuple[set[str], set[str]]:
    tokenizer, pipe = get_skills_model()
    chunks = create_overlapping_chunks(text, tokenizer, max_tokens, overlap_tokens)
    model = get_keybert_model()

    unigrams = model.extract_keywords(
        chunks,
        keyphrase_ngram_range=(1, 1),
        use_mmr=True,
        diversity=0.7,
        top_n=top_n
    )

    bigrams = model.extract_keywords(
        chunks,
        keyphrase_ngram_range=(2, 2),
        use_mmr=True,
        diversity=0.7,
        top_n=top_n
    )

    all_keywords = unigrams + bigrams
    if all_keywords and isinstance(all_keywords[0], tuple):
        all_keywords = [all_keywords]

    filtered_keywords = set()
    for keywords in all_keywords:
        for keyword, _ in keywords:
            if not is_repeated_word(keyword):
                filtered_keywords.add(keyword.lower())

    if extract_skills:
        skills = set()
        for chunk in chunks:
            chunk_skills = extract_chunk_skills(chunk, pipe)
            skills = skills.union(chunk_skills)

        skills = filtered_keywords.intersection(skills)
        return filtered_keywords, skills

    return filtered_keywords
