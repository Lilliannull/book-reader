from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import os
from extractors import extract_text_by_extension

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
    return HTMLResponse(f"""
        <h2>Extracted Content from {file.filename}</h2>
        <div style='white-space: pre-wrap; max-width: 800px; margin: auto; font-family: sans-serif;'>
            {extracted}
        </div>
        <br><a href='/'>⬅ Back</a>
    """)
