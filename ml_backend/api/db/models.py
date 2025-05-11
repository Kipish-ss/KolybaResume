from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy import Text as TextType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    Id = Column(Integer, primary_key=True, index=True)
    Uid = Column(String, index=True)
    Name = Column(String(50))
    Email = Column(String(50))


class Resume(Base):
    __tablename__ = "Resumes"

    Id = Column(Integer, primary_key=True, index=True)
    UserId = Column(Integer, ForeignKey("Users.Id"))
    Text = Column(TextType)
    CleanedText = Column(TextType, nullable=True)
    Vector = Column(LargeBinary, nullable=True)
    Category = Column(Integer, nullable=True)


class Vacancy(Base):
    __tablename__ = "Vacancies"

    Id = Column(Integer, primary_key=True, index=True)
    Title = Column(TextType)
    Text = Column(TextType)
    Vector = Column(LargeBinary, nullable=True)
    Category = Column(Integer, nullable=True)
    CleanedText = Column(TextType, nullable=True)
