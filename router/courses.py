import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from repositories.courses import CourseRepository
from schemas import SCourseCreate, SCourseMaterialAdd, SCourseTestAdd




courses_router = APIRouter(
    prefix="/courses",
    tags=['Курсы']
)


@courses_router.post("/create")
async def create_course(course_data: SCourseCreate):
    course_id = await CourseRepository.create_course(course_data.title, course_data.description, course_data.image_url)
    return {"success": True, "course_id": course_id}


@courses_router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    file_path = await CourseRepository.upload_file(file)
    return {"success": True, "file_path": file_path}


@courses_router.post("/add-material")
async def add_material(material_data: SCourseMaterialAdd):
    if material_data.type == "file" and not os.path.exists(material_data.content):
        raise HTTPException(status_code=400, detail="Файл не найден")

    await CourseRepository.add_material(material_data.course_id, material_data.type, material_data.content, material_data.title)
    return {"success": True}


@courses_router.post("/add-test")
async def add_test(test_data: SCourseTestAdd):
    await CourseRepository.add_test(test_data.course_id, test_data.question, test_data.options, test_data.correct_answer)
    return {"success": True}


@courses_router.get("/{course_id}")
async def get_course(course_id: int):
    course = await CourseRepository.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Курс не найден")
    return course


@courses_router.get("/")
async def get_all_courses():
    courses = await CourseRepository.get_all_courses()
    return courses