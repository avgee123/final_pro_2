from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from database import SessionLocal
from sqlalchemy.orm import Session
from database import EventFind
from geopy.geocoders import Nominatim
import googlemaps
import models
from dotenv import load_dotenv
import os

router = APIRouter(prefix='/event', tags=['/event'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#minta geolocator untuk carikan berdasarkan location, event type kita
#geolocator tahunya kalo location nnti dipulangkan dalam longitude, langitude, 

load_dotenv()
api_key = os.getenv("API_KEY_GEO")
geolocator = Nominatim(user_agent="orbit_personal_app")
gmaps = googlemaps.Client(api_key)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/search", status_code=status.HTTP_201_CREATED)
def rekomendasi_events(db: db_dependency, request: EventFind):
    location_first = geolocator.geocode(request.location)

    if not location_first:
        raise HTTPException(status_code=404, detail="Lokasi tidak dapat ditemukan")
    
    search_query = f"{request.event_type} in {location_first.address}"
    coordinates = (location_first.latitude, location_first.longitude)
    places_found = gmaps.places(query=search_query, location=coordinates, radius=10000)

    rekomendasi = []

    for place in places_found.get("results", []):
        geo = place.get("geometry")
        loc = geo.get("location")

        rekomendasi.append({
            "name" : place.get("name"),
            "address" : place.get("formatted_address"),
            "latitude" : loc.get("lat"),
            "longitude" : loc.get("lng"),
            "rating" : place.get("rating")
        })

    new_event = models.ReportedEvents(location = request.location,
                                      latitude = location_first.latitude,
                                      longitude = location_first.longitude,
                                      event_type = request.event_type
    )

    db.add(new_event)
    db.commit()

    return {

        "message" : rekomendasi
    }



