from fastapi import APIRouter
from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from app.db_models import DataPoint
from app.dependencies import DatabaseSession
from app.dependencies import _Session
from app.dependencies import templates
from app.schemas import DataPointSchema

# Seed database with initial data (demo purposes)
try:
    db = _Session()
    if db.query(DataPoint).count() == 0:
        from datetime import timedelta
        import random
        for i in range(10):
            dp = DataPoint(
                value= round(random.uniform(0, 100), 2),
                timestamp=datetime.utcnow() - timedelta(days=(10 - i))
            )
            db.add(dp)
        db.commit()
finally:
    db.close()


router = APIRouter(prefix="/data")

@router.get("/list", response_class=HTMLResponse)
def get_data_list(request: Request, db: DatabaseSession):
    """Return HTML list of data points for HTMX partial update."""
    items = db.query(DataPoint).order_by(DataPoint.timestamp.desc()).all()
    return templates.TemplateResponse("data_list.jinja", {"request": request, "items": items})

@router.post("/add", response_class=HTMLResponse)
def add_data(request: Request, db: DatabaseSession, value: float = Form(...)):
    """Handle form submission to add a new data point."""
    new_dp = DataPoint(value=value, timestamp=datetime.utcnow())
    db.add(new_dp)
    db.commit()
    db.refresh(new_dp)
    # Return updated list of data points as HTML
    items = db.query(DataPoint).order_by(DataPoint.timestamp.desc()).all()
    return templates.TemplateResponse("data_list.jinja", {"request": request, "items": items})

@router.get("/", response_model=list[DataPointSchema])
def get_data_api(db: DatabaseSession):
    """API endpoint to retrieve data points as JSON (for charts)."""
    points = db.query(DataPoint).order_by(DataPoint.timestamp).all()
    # Convert to Pydantic schema objects for JSON serialization
    return [DataPointSchema.from_orm(p) for p in points]