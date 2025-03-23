from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Model




class CourseOrm(Model):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    image_url: Mapped[str]
    short_description: Mapped[str]
    content: Mapped[str]
    video_url: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    tests: Mapped[list["TestOrm"]] = relationship(back_populates="course")


class TestOrm(Model):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    title: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    questions: Mapped[list["QuestionOrm"]] = relationship(back_populates="test")
    course: Mapped["CourseOrm"] = relationship(back_populates="tests")


class QuestionOrm(Model):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'))
    text: Mapped[str]
    options: Mapped[str]
    correct_answer: Mapped[str]

    test: Mapped["TestOrm"] = relationship(back_populates="questions")


class UserProgressOrm(Model):
    __tablename__ = 'user_progress'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'))
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())