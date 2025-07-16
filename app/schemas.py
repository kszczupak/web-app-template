from pydantic import BaseModel
from datetime import datetime

class DataPointSchema(BaseModel):
    id: int
    timestamp: datetime
    value: float
    class Config:
        orm_mode = True