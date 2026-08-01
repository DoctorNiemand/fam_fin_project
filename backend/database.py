from sqlalchemy import create_engine
from models.base import Base

engine = create_engine("sqlite:///finance.db")
Base.metadata.create_all(engine)

