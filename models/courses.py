from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Model




class CourseOrm(Model):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    image_url: Mapped[str] = mapped_column(nullable=True)  # Ссылка на фото курса
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    # Связь с материалами курса
    materials: Mapped[list["CourseMaterialOrm"]] = relationship(back_populates="course")
    tests: Mapped[list["CourseTestOrm"]] = relationship(back_populates="course")


class CourseMaterialOrm(Model):
    __tablename__ = 'course_materials'

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    type: Mapped[str]  # Тип материала: video, text, file
    content: Mapped[str]  # Ссылка на видео, текст или файл
    title: Mapped[str]  # Название материала

    course: Mapped["CourseOrm"] = relationship(back_populates="materials")


class CourseTestOrm(Model):
    __tablename__ = 'course_tests'

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    question: Mapped[str]
    options: Mapped[str]  # JSON строка с вариантами ответов
    correct_answer: Mapped[str]  # Правильный ответ

    course: Mapped["CourseOrm"] = relationship(back_populates="tests")