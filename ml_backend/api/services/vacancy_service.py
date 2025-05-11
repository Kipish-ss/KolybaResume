from sqlalchemy import select
from sqlalchemy.orm import Session
from ml_backend.api.db.models import Vacancy, Resume
from ml_backend.api.models.schemas import VacancyScoreResponse, ResumeVacancyMatch
from ml_backend.api.services.cleaning_service import clean_text, translate
from ml_backend.api.services.model_service import get_embedding_model
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def store_vacancy_vectors(db: Session, vacancy_ids: list[int]) -> list[VacancyScoreResponse]:
    if not vacancy_ids:
        return []

    model = get_embedding_model()
    results = []

    stmt = select(Vacancy).where(Vacancy.Id.in_(vacancy_ids))
    vacancies = db.execute(stmt).scalars().all()
    vacancy_vectors = {}

    for vacancy in vacancies:
        vacancy_text = f"{vacancy.Title} {vacancy.Text} {vacancy.Location or ''}"
        vacancy_text = translate(vacancy_text)
        cleaned_vacancy_text = clean_text(vacancy_text)
        vacancy_vector = model.encode(cleaned_vacancy_text)

        vacancy_vectors[vacancy.Id] = vacancy_vector
        vacancy.Vector = vacancy_vector.tobytes()

    db.commit()

    categories = {vacancy.Category for vacancy in vacancies if vacancy.Category is not None}
    stmt = select(Resume).where(
        Resume.Category.in_(categories),
        Resume.Vector.is_not(None)
    )
    matching_resumes = db.execute(stmt).scalars().all()

    resumes_by_category = {}
    for resume in matching_resumes:
        if resume.Category not in resumes_by_category:
            resumes_by_category[resume.Category] = []
        resumes_by_category[resume.Category].append(resume)

    for vacancy in vacancies:
        if vacancy.Category is None or vacancy.Category not in resumes_by_category:
            continue

        vacancy_vector = vacancy_vectors[vacancy.Id]
        category_resumes = resumes_by_category[vacancy.Category]

        for resume in category_resumes:
            resume_vector = np.frombuffer(resume.Vector, dtype=np.float32)
            similarity = model.similarity(vacancy_vector, resume_vector)[0][0]
            score = int(similarity * 100)

            results.append(
                VacancyScoreResponse(
                    user_id=resume.UserId,
                    vacancy_id=vacancy.Id,
                    score=score
                )
            )

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
