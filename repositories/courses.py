import os
import uuid
from fastapi import UploadFile
from database import new_session
from models.courses import CourseOrm, TestOrm, QuestionOrm, UserProgressOrm
from sqlalchemy import select
import json
from schemas import SQuestion




class CourseRepository:
    # Папка для загрузки изображений курсов
    UPLOAD_DIR = "uploads/courses/images"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    @classmethod
    async def upload_image(cls, file: UploadFile) -> str:
        # Генерация уникального имени файла
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(cls.UPLOAD_DIR, unique_filename)

        # Сохранение файла на сервере
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path

    @classmethod
    async def create_course(cls, title: str, image_file: UploadFile, short_description: str, content: str, video_url: str):
        # Загружаем изображение
        image_path = await cls.upload_image(image_file)

        async with new_session() as session:
            course = CourseOrm(
                title=title,
                image_url=image_path,  # Сохраняем путь к изображению
                short_description=short_description,
                content=content,
                video_url=video_url
            )
            session.add(course)
            await session.commit()
            return course.id


    @classmethod
    async def get_course(cls, course_id: int):
        async with new_session() as session:
            query = select(CourseOrm).where(CourseOrm.id == course_id)
            result = await session.execute(query)
            return result.scalars().first()


    @classmethod
    async def get_all_courses(cls, limit: int, offset: int):
        async with new_session() as session:
            query = select(CourseOrm).limit(limit).offset(offset)
            result = await session.execute(query)
            return result.scalars().all()



class TestRepository:
    @classmethod
    async def create_test(cls, course_id: int, title: str, questions: list[SQuestion]):  # Используем SQuestion
        async with new_session() as session:
            test = TestOrm(course_id=course_id, title=title)
            session.add(test)
            await session.flush()  # Получаем ID теста

            # Добавляем вопросы
            for question in questions:
                question_orm = QuestionOrm(
                    test_id=test.id,
                    text=question.text,  # Используем точечную нотацию
                    options=json.dumps(question.options),  # Используем точечную нотацию
                    correct_answer=question.correct_answer  # Используем точечную нотацию
                )
                session.add(question_orm)

            await session.commit()
            return test.id


    @classmethod
    async def get_test(cls, test_id: int):
        async with new_session() as session:
            query = select(TestOrm).where(TestOrm.id == test_id)
            result = await session.execute(query)
            return result.scalars().first()



class UserProgressRepository:
    @classmethod
    async def mark_test_completed(cls, user_id: int, test_id: int):
        async with new_session() as session:
            progress = UserProgressOrm(user_id=user_id, test_id=test_id, is_completed=True)
            session.add(progress)
            await session.commit()


    @classmethod
    async def get_user_progress(cls, user_id: int):
        async with new_session() as session:
            query = select(UserProgressOrm).where(UserProgressOrm.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()
    
    
    @classmethod
    async def get_user_progress_by_course(cls, user_id: int, course_id: int):
        async with new_session() as session:
            # Получаем все тесты для курса
            query = select(TestOrm).where(TestOrm.course_id == course_id)
            result = await session.execute(query)
            tests = result.scalars().all()

            # Получаем прогресс пользователя по каждому тесту
            progress = []
            for test in tests:
                query = select(UserProgressOrm).where(
                    (UserProgressOrm.user_id == user_id) &
                    (UserProgressOrm.test_id == test.id)
                )
                result = await session.execute(query)
                user_progress = result.scalars().first()

                progress.append({
                    "test_id": test.id,
                    "test_title": test.title,
                    "is_completed": user_progress.is_completed if user_progress else False
                })

            return progress