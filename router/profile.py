from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from security import get_current_user
from models.auth import UserOrm
from repositories.profile import CVRepository
import os




profile_router = APIRouter(
    prefix="/auth",
    tags=['Профиль']
)

@profile_router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), current_user: UserOrm = Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Файл должен быть в формате PDF")

    file_path = f"uploads/cvs/cv_{current_user.id}.pdf"
    os.makedirs("uploads/cvs", exist_ok=True)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    await CVRepository.save_cv(current_user.id, file_path)
    return {"success": True, "message": "Резюме успешно загружено"}


@profile_router.get("/download-resume")
async def download_resume(current_user: UserOrm = Depends(get_current_user)):
    cv = await CVRepository.get_cv_by_user_id(current_user.id)
    if not cv:
        raise HTTPException(status_code=404, detail="Резюме не найдено")

    return FileResponse(cv.file_path, media_type="application/pdf", filename=f"cv_{current_user.id}.pdf")