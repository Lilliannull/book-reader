from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import os
from extractors import extract_text_by_extension

import re

def is_english_text(text):
    letters = re.findall(r'[a-zA-Z]', text)
    ratio = len(letters) / max(len(text), 1)
    return ratio > 0.7  # 英文字符比例超过 70% 就认为是英文

def mock_translate(paragraph):
    return f"（翻译）{paragraph}"  # 你之后可以替换成真实翻译接口

def translate_paragraphs(text):
    if not is_english_text(text):
        return None  # 不是英文就不翻译

    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    translated_blocks = []
    for para in paragraphs:
        zh = mock_translate(para)
        translated_blocks.append((para, zh))
    return translated_blocks


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
 