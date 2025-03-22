from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Model




class CourseOrm(Model):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]  # Название курса
    image_url: Mapped[str]  # Путь к фото курса
    short_description: Mapped[str]  # Краткое описание
    content: Mapped[str]  # Основной текст (markdown)
    video_url: Mapped[str]  # Ссылка на видео
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    # Связь с тестами
    tests: Mapped[list["TestOrm"]] = relationship(back_populates="course")


class TestOrm(Model):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    title: Mapped[str]  # Название теста
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    # Связь с вопросами
    questions: Mapped[list["QuestionOrm"]] = relationship(back_populates="test")
    # Связь с курсом
    course: Mapped["CourseOrm"] = relationship(back_populates="tests")


class QuestionOrm(Model):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'))
    text: Mapped[str]  # Текст вопроса
    options: Mapped[str]  # JSON строка с вариантами ответов
    correct_answer: Mapped[str]  # Правильный ответ

    # Связь с тестом
    test: Mapped["TestOrm"] = relationship(back_populates="questions")


class UserProgressOrm(Model):
    __tablename__ = 'user_progress'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'))
    is_completed: Mapped[bool] = mapped_column(default=False)  # Пройден ли тест
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())