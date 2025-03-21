from database import new_session
from models.profile import CVOrm
from sqlalchemy import select




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