from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ścieżka do katalogu ze statycznymi plikami (HTML, JS, CSS)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Montowanie plików statycznych pod URL `/static`
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Endpoint serwujący główną stronę aplikacji (index.html)
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path, media_type="text/html")
    else:
        raise HTTPException(status_code=404, detail="Index page not found")

# Przykładowy endpoint API – zwraca prosty komunikat (wykorzystany przez Lit na froncie)
@app.get("/api/hello", response_class=JSONResponse)
def api_hello():
    message = "Hello from FastAPI backend!"
    return {"message": message}

# (Opcjonalnie) Endpoint testowy bazy danych – np. proste sprawdzenie połączenia
# Zakładamy, że zmienne DB_* są ustawione; tutaj tylko przykład składni.
@app.get("/api/db-check", response_class=JSONResponse)
def db_check():
    db_host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "")
    return {"db_host": db_host, "db_name": db_name, "status": "ok"}

# Uwaga: Podczas developmentu uruchamiamy aplikację komendą uvicorn (np. przez docker-compose lub IDE).
# W produkcji aplikacja będzie uruchamiana przez Gunicorn (zgodnie z konfiguracją w Dockerfile).
