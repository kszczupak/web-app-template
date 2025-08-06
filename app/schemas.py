from pydantic import BaseModel
from datetime import datetime

class DataPointSchema(BaseModel):
    id: int
    timestamp: datetime
    value: float
    class Config:
        from_attributes = True