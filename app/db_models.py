from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime

from app.dependencies import Base


class DataPoint(Base):
    __tablename__ = "data_points"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    value = Column(Float, nullable=False)