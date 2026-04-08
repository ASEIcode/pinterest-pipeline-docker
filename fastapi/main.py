import fastapi
from models import UserData, PinData, GeoData

app = fastapi.FastAPI()

# Pindata endpoint
@app.post("/pindata/")
def create_pindata(pin_data: PinData):
    return pin_data
# GeoData endpoint
@app.post("/geodata/")
def create_geodata(geo_data: GeoData):
    return geo_data
# UserData endpoint
@app.post("/userdata/")
def create_userdata(user_data: UserData):
    return user_data