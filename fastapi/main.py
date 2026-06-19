import fastapi
from models import UserData, PinData, GeoData
from kafka import KafkaProducer #import the KafkaProducer class from the kafka library to send messages to a Kafka topic
import json #import the json library to convert Python objects to JSON format
import datetime

app = fastapi.FastAPI()

# Define a custom function to serialize datetime objects
def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x, default=serialize_datetime).encode('utf-8')
)

# Pindata endpoint
@app.post("/pindata/")
def create_pindata(pin_data: PinData):
    producer.send('pinterest.pin', value=pin_data.dict())
    return pin_data
# GeoData endpoint
@app.post("/geodata/")
def create_geodata(geo_data: GeoData):
    producer.send('pinterest.geo', value=geo_data.dict())
    return geo_data
# UserData endpoint
@app.post("/userdata/")
def create_userdata(user_data: UserData):
    producer.send('pinterest.user', value=user_data.dict())
    return user_data