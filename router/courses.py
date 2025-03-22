from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from security import get_current_user
from models.auth import UserOrm
from repositories.courses import CourseRepository, TestRepository, UserProgressRepository
from schemas import SCourseCreate, STestCreate, SQuestion




courses_router = APIRouter(
    prefix="/courses",
    tags=['Курсы']
)



@courses_router.post("/create")
async def create_course(
    title: str = Form(...),
    short_description: str = Form(...),
    content: str = Form(...),
    video_url: str = Form(...),
    image_file: UploadFile = File(...),
    current_user: UserOrm = Depends(get_current_user)
):
    # Создаем курс с загруженным изображением
    course_id = await CourseRepository.create_course(
        title=title,
        image_file=image_file,
        short_description=short_description,
        content=content,
        video_url=video_url
    )
    return {"success": True, "course_id": course_id}


@courses_router.post("/add-test")
async def add_test(test_data: STestCreate):
    test_id = await TestRepository.create_test(
        course_id=test_data.course_id,
        title=test_data.title,
        questions=test_data.questions
    )
    return {"success": True, "test_id": test_id}


@courses_router.post("/complete-test")
async def complete_test(test_id: int, current_user: UserOrm = Depends(get_current_user)):
    await UserProgressRepository.mark_test_completed(current_user.id, test_id)
    return {"success": True}


@courses_router.get("/{course_id}")
async def get_course(course_id: int):
    course = await CourseRepository.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    return course


@courses_router.get("/")
async def get_all_courses(limit: int=10, offset: int=0):
    courses = await CourseRepository.get_all_courses(limit, offset)
    return courses


@courses_router.get("/{course_id}/progress")
async def get_course_progress(course_id: int, current_user: UserOrm = Depends(get_current_user)):
    progress = await UserProgressRepository.get_user_progress_by_course(current_user.id, course_id)
    return {"success": True, "progress": progress}