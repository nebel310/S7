from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List
from datetime import datetime




class SUserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class SCourseCreate(BaseModel):
    title: str
    image_url: str
    short_description: str
    content: str  # Markdown текст
    video_url: str


class SQuestion(BaseModel):
    text: str  # Текст вопроса
    options: List[str]  # Варианты ответов
    correct_answer: str  # Правильный ответ


class STestCreate(BaseModel):
    course_id: int
    title: str
    questions: List[SQuestion]  # Список вопросов


class SUserProgress(BaseModel):
    test_id: int
    test_title: str
    is_completed: bool


class SCourseProgressResponse(BaseModel):
    success: bool
    progress: List[SUserProgress]

    


class SPhotoResult(BaseModel):
    success: bool
    result: int
    photo_path: str