import enum
from typing import List
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime, timezone

from .database import Base


class UserRole(enum.Enum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    TUTOR = "tutor"
    STUDENT = "student"


class QuestionSection(enum.Enum):
    A = "A"
    B = "B"


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    questions: Mapped[List["Question"]] = relationship(back_populates="module")
    study_manuals: Mapped[List["StudyManual"]] = relationship(back_populates="module")


class StudyManual(Base):
    __tablename__ = "study_manuals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"))
    module: Mapped["Module"] = relationship(back_populates="study_manuals")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    section: Mapped[QuestionSection] = mapped_column(Enum(QuestionSection))
    title: Mapped[str] = mapped_column()
    question_text: Mapped[str] = mapped_column()
    marking_schema: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"))
    module: Mapped["Module"] = relationship(back_populates="questions")

    answers: Mapped[List["Answer"]] = relationship(back_populates="question")


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    answer_text: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    student: Mapped["User"] = relationship(back_populates="answers")

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    question: Mapped["Question"] = relationship(back_populates="answers")

    mark: Mapped["Mark"] = relationship(back_populates="answer")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    fullname: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    answers: Mapped[List["Answer"]] = relationship(back_populates="student")
    given_marks: Mapped[List["Mark"]] = relationship(back_populates="tutor")


class Mark(Base):
    __tablename__ = "marks"
    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 100", name="check_score_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    score: Mapped[int] = mapped_column()
    feedback: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"), unique=True)
    answer: Mapped["Answer"] = relationship(back_populates="mark", single_parent=True)

    tutor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tutor: Mapped["User"] = relationship(back_populates="given_marks")
