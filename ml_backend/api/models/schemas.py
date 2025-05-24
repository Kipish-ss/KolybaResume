from pydantic import BaseModel


class UserBase(BaseModel):
    uid: str
    name: str
    email: str

    class Config:
        from_attributes = True


class User(UserBase):
    id: int | None


class ResumeBase(BaseModel):
    user_id: int
    text: str
    cleared_text: str | None
    category: int | None

    class Config:
        from_attributes = True


class ResumeCreate(ResumeBase):
    pass


class Resume(ResumeBase):
    id: int


class ResumeWithVector(Resume):
    vector: bytes


class VacancyBase(BaseModel):
    title: str
    text: str
    url: str
    salary: str | None
    location: str | None
    category: int | None

    class Config:
        from_attributes = True


class VacancyCreate(VacancyBase):
    pass


class Vacancy(VacancyBase):
    id: int


class VacancyWithVector(Vacancy):
    vector: bytes


class Company(BaseModel):
    url: str
    id: int | None

    class Config:
        from_attributes = True


class ResumeRequest(BaseModel):
    resume_id: int


class VacanciesRequest(BaseModel):
    vacancy_ids: list[int] | None


class VacancyScoreResponse(BaseModel):
    user_id: int
    vacancy_id: int
    score: int


class ResumeVacancyMatch(BaseModel):
    vacancy_id: int
    score: int


class AdaptationRequest(BaseModel):
    resume_id: int
    vacancy_text: str


class AdaptationResponse(BaseModel):
    score: int
    missing_keywords: list[str] | None


class VectorInput(BaseModel):
    vector: bytes


class CategoryEnum(BaseModel):
    id: int
    name: str
