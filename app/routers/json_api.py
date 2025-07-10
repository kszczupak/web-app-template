from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter(prefix="/api")

# Przykładowy endpoint API – zwraca prosty komunikat (wykorzystany przez Lit na froncie)
@router.get("/hello", response_class=JSONResponse)
def api_hello():
    message = "Hello from FastAPI backend!"
    return {"message": message}

