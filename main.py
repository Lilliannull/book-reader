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
    <html>
    <head>
        <title>{file.filename}</title>
        <script>
            function readAloud() {{
                const text = document.getElementById("book-content").innerText.slice(0, 1000);
                const utter = new SpeechSynthesisUtterance(text);
                utter.lang = "en-US";
                speechSynthesis.cancel();
                speechSynthesis.speak(utter);
            }}
        </script>
    </head>
    <body>
        <h2>{file.filename}</h2>
        <button onclick="readAloud()">🔈 Read Aloud</button>
        <pre id="book-content">{extracted}</pre>
        <br><a href="/">⬅ Back</a>
    </body>
    </html>
    """)
