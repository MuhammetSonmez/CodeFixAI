import os
from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from models import model
from config import SUPPORTED_LANGUAGES, SOLUTIONS_DIR

router = APIRouter()
templates = Jinja2Templates(directory="templates")

os.makedirs(SOLUTIONS_DIR, exist_ok=True)

@router.get("/")
async def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/debug")
async def debug_code(
    file: UploadFile = File(None),
    code: str = Form(None),
    lang: str = Form(None)
):
    if file:
        content = await file.read()
        code = content.decode("utf-8")
        filename = file.filename
        ext = filename.split(".")[-1]
        lang = SUPPORTED_LANGUAGES.get(ext, None)
    else:
        filename = "code.txt"

    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    if not lang:
        raise HTTPException(status_code=400, detail="Language not specified or unsupported")

    response = model.debug(lang=lang, code=code)

    fixed_filename = os.path.join(SOLUTIONS_DIR, f"fixed_{filename}")
    with open(fixed_filename, "w", encoding="utf-8") as f:
        f.write(response)

    return {"fixed_code": response, "download": f"/download/fixed_{filename}"}

@router.get("/download/{filename}")
async def download_fixed_code(filename: str):
    file_path = os.path.join(SOLUTIONS_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, media_type="text/plain", filename=filename)
