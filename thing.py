from sqlalchemy import Table, Column, Integer, String
from config.db import Base
from pydantic import BaseModel

#SQL 
class ThingModel(Base):
    __tablename__ = "things"

    thing_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    board_pin = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
