from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Model




class CVOrm(Model):
    __tablename__ = 'cvs'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    file_path: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())


class PhotoResultOrm(Model):
    __tablename__ = 'photo_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    photo_path: Mapped[str]
    result: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())