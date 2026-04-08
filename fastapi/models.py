from pydantic import BaseModel
from datetime import datetime

class PinData(BaseModel):
    index: int
    unique_id: str
    title: str
    description: str
    poster_name: str
    follower_count: int
    tag_list: str
    is_image_or_video: str
    image_src: str
    downloaded: int
    save_location: str
    category: str

class GeoData(BaseModel):
    ind: int
    timestamp: datetime
    latitude: float
    longitude: float
    country: str

class UserData(BaseModel):
    ind: int
    first_name: str
    last_name: str
    age: int
    date_joined: datetime
 