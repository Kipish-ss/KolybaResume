from sqlalchemy import select
from sqlalchemy.orm import Session
from ml_backend.api.db.models import Vacancy, Resume
from ml_backend.api.models.schemas import VacancyScoreResponse, ResumeVacancyMatch
from ml_backend.api.services.cleaning_service import clean_text, translate
from ml_backend.api.services.model_service import get_embedding_model
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict


def store_vacancy_vectors(db: Session, vacancy_ids: list[int], batch_size: int = 32) -> list[VacancyScoreResponse]:
    if not vacancy_ids:
        return []

    model = get_embedding_model()
    stmt = select(Vacancy).where(Vacancy.Id.in_(vacancy_ids))
    vacancies = db.execute(stmt).scalars().all()

    vacancy_texts = []
    for vacancy in vacancies:
        text = translate(f"{vacancy.Title} {vacancy.Text}")
        cleaned = clean_text(text)
        vacancy.CleanedText = cleaned
        vacancy_texts.append(cleaned)

    vacancy_vectors = {}
    for i in range(0, len(vacancies), batch_size):
        batch_texts = vacancy_texts[i:i + batch_size]
        batch_vacancies = vacancies[i:i + batch_size]

        encoded_batch = model.encode(batch_texts)

        for j, vacancy in enumerate(batch_vacancies):
            vector = encoded_batch[j]
            vacancy.Vector = vector.tobytes()
            vacancy_vectors[vacancy.Id] = vector

    db.commit()

    categories = {v.Category for v in vacancies if v.Category is not None}
    if not categories:
        return []

    stmt = select(Resume).where(
        Resume.Category.in_(categories),
        Resume.Vector.is_not(None)
    )
    matching_resumes = db.execute(stmt).scalars().all()

    if not matching_resumes:
        return []

    resumes_by_category = defaultdict(list)
    resume_vectors = {}

    for resume in matching_resumes:
        resumes_by_category[resume.Category].append(resume)
        resume_vectors[resume.Id] = np.frombuffer(resume.Vector, dtype=np.float32)

    results = []
    for vacancy in vacancies:
        vacancy_category = vacancy.Category
        if vacancy_category not in resumes_by_category:
            continue

        vacancy_vector = vacancy_vectors[vacancy.Id]
        for resume in resumes_by_category[vacancy_category]:
            resume_vector = resume_vectors[resume.Id]
            similarity = model.similarity(vacancy_vector, resume_vector)[0][0]
            score = int(similarity * 100)

            results.append(VacancyScoreResponse(
                user_id=resume.UserId,
                vacancy_id=vacancy.Id,
                score=score
            ))

    return results


def get_matches_for_resume(db: Session, resume_id: int) -> list[ResumeVacancyMatch]:
    resume = db.get(Resume, resume_id)

    if not resume or not resume.Vector or resume.Category is None:
        return []

    stmt = select(Vacancy).where(
        Vacancy.Category == resume.Category,
        Vacancy.Vector.is_not(None)
    )
    result = db.execute(stmt)
    matching_vacancies = result.scalars().all()

    if not matching_vacancies:
        return []

    resume_vector = np.frombuffer(resume.Vector, dtype=np.float32)

    results = []
    for vacancy in matching_vacancies:
        vacancy_vector = np.frombuffer(vacancy.Vector, dtype=np.float32)

        similarity = cosine_similarity(
            resume_vector.reshape(1, -1),
            vacancy_vector.reshape(1, -1)
        )[0][0]

        score = int(similarity * 100)

        results.append(
            ResumeVacancyMatch(
                vacancy_id=vacancy.Id,
                score=score
            )
        )

    results.sort(key=lambda x: x.score, reverse=True)

    return results[:200]
