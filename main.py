from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from langdetect import detect
import shutil
import os
import re
from extractors import extract_text_by_extension
from translator import translate
from fastapi.responses import JSONResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted = extract_text_by_extension(file_path)
    paragraphs = [p.strip() for p in extracted.split('\n\n') if p.strip()]

    return templates.TemplateResponse("read_page.html", {
        "request": request,
        "file_name": file.filename,
        "paragraphs": paragraphs
    })

@app.post("/translate")
async def translate_paragraph(request: Request):
    data = await request.json()
    text = data.get("text", "")

    try:
        translated = translate(text)
        return JSONResponse({"translation": translated})
    except Exception as e:
        return JSONResponse({"translation": "❌ 翻译失败", "error": str(e)})
 
