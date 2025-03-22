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
    description: str
    image_url: str | None = None


class SCourseMaterialAdd(BaseModel):
    course_id: int
    type: str
    content: str
    title: str


class SCourseTestAdd(BaseModel):
    course_id: int
    question: str
    options: List[str]
    correct_answer: str
    


class SPhotoResult(BaseModel):
    success: bool
    result: int
    photo_path: str