from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

database_url = "postgresql://postgres:Astridisblessed_19071978@localhost:5432/final_pro"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Activity(BaseModel):
    title : str
    description : str
    lcoation : str
    image_url : str

class EventFind(BaseModel):
    location: str
    event_type: str

    
class Advice(BaseModel):
    user_say: str

