from fastapi import UploadFile
from database import new_session
from models.courses import CourseOrm, CourseMaterialOrm, CourseTestOrm
from sqlalchemy import select
import os
import uuid




class CourseRepository:
    # Папка для загрузки файлов
    UPLOAD_DIR = "uploads/courses/material"
    os.makedirs(UPLOAD_DIR, exist_ok=True)


    @classmethod
    async def create_course(cls, title: str, description: str, image_url: str = None):
        async with new_session() as session:
            course = CourseOrm(title=title, description=description, image_url=image_url)
            session.add(course)
            await session.commit()
            return course.id


    @classmethod
    async def add_material(cls, course_id: int, material_type: str, content: str, title: str):
        async with new_session() as session:
            material = CourseMaterialOrm(course_id=course_id, type=material_type, content=content, title=title)
            session.add(material)
            await session.commit()


    @classmethod
    async def add_test(cls, course_id: int, question: str, options: list[str], correct_answer: str):
        async with new_session() as session:
            test = CourseTestOrm(course_id=course_id, question=question, options=str(options), correct_answer=correct_answer)
            session.add(test)
            await session.commit()


    @classmethod
    async def get_course(cls, course_id: int):
        async with new_session() as session:
            query = select(CourseOrm).where(CourseOrm.id == course_id)
            result = await session.execute(query)
            return result.scalars().first()


    @classmethod
    async def get_all_courses(cls):
        async with new_session() as session:
            query = select(CourseOrm)
            result = await session.execute(query)
            return result.scalars().all()


    @classmethod
    async def upload_file(cls, file: UploadFile):
        # Генерация уникального имени файла
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(cls.UPLOAD_DIR, unique_filename)

        # Сохранение файла на сервере
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path