import os
import uuid
from database import new_session
from models.profile import CVOrm, PhotoResultOrm
from sqlalchemy import select
from fastapi import UploadFile
from deploy import Predict




class CVRepository:
    @classmethod
    async def save_cv(cls, user_id: int, file_path: str):
        async with new_session() as session:
            cv = CVOrm(user_id=user_id, file_path=file_path)
            session.add(cv)
            await session.commit()


    @classmethod
    async def get_cv_by_user_id(cls, user_id: int):
        async with new_session() as session:
            query = select(CVOrm).where(CVOrm.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().first()



class PhotoRepository:
    # Папка для загрузки фотографий
    UPLOAD_DIR = "uploads/profile/photos"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    @classmethod
    async def save_photo_result(cls, user_id: int, photo_path: str, result: int):
        async with new_session() as session:
            photo_result = PhotoResultOrm(user_id=user_id, photo_path=photo_path, result=result)
            session.add(photo_result)
            await session.commit()


    @classmethod
    async def upload_photo(cls, file: UploadFile):
        # Генерация уникального имени файла
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(cls.UPLOAD_DIR, unique_filename)

        # Сохранение файла на сервере
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path


    @classmethod
    async def process_photo_with_nn(cls, photo_path: str):
        # Создаем временный файл для вывода результата
        output_file = os.path.join(cls.UPLOAD_DIR, "temp_output.txt")

        # Вызываем ваш класс Predict
        predictor = Predict(photo_path, output_file)
        predictor.make_prediction()

        # Читаем результат из файла
        with open(output_file, 'r') as f:
            result = int(f.read().strip())

        # Удаляем временный файл
        os.remove(output_file)

        return result