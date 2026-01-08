from datetime import datetime
import os
from typing import Optional
from click import File
from database import SessionLocal
from database import Advice
from fastapi import APIRouter,FastAPI,HTTPException, UploadFile
from fastapi.params import Depends, Form
import models
from starlette import status
from sqlalchemy.orm import Session

router = APIRouter(prefix='/achivements', tags=['achivements'])

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/', status_code=status.HTTP_201_CREATED)
def post_activity(title: str = Form(...),
                  description: str = Form(...),
                  location: str = Form(...),
                  file: Optional[UploadFile] = File(None),
                  db: Session = Depends(get_db)
                  ):
    
    #uplading file
    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = None

    if (file is not None and file.file is not None and file.filename):
        timestamp = datetime.now().strftime("%Y%M%d%H%M%S")
        file_name = f"{timestamp}_{file.filename}"
        file_path = os.path.join(upload_dir, file_name)


    new_activity = models.Achivements(
        title = title,
        description = description,
        location = location,
        image_url = file_path,
    )

    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

@router.get('/', status_code=status.HTTP_200_OK)
def get_activities(db: Session = Depends(get_db)):

    activities = db.query(models.Achivements).order_by(models.Achivements.created_at).all()

    for activity in activities:
        if activity.image_url:
            activity.image_url = activity.image_url.replace("\\", "/")

    return activities


from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})

@router.post("/advice")
def get_ai_advice(request: Advice, db: Session = Depends(get_db)):

    activities = db.query(models.Achivements).order_by(models.Achivements.created_at).all()
    list_to_text = "\n".join([f"- {a.title}: {a.description}" for a in activities]) 

    prompt = (
        f"User feels this way today: {request.user_say}.\n"
        f"Therefore, based on the activities {list_to_text},\n"
        f"As a soul and heart psychologist, give advice or suggestion or mood maker messages for user"
    )
    
    response = client.models.generate_content(model="models/gemini-2.5-flash", contents=prompt)
    
    new_entry = models.AIAdvice(user_say = request.user_say)

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "message" : response.text
    }

