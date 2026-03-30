from faker import Faker #import the Faker library to generate fake data for testing purposes
from kafka import KafkaProducer #import the KafkaProducer class from the kafka library to send messages to a Kafka topic
import json #import the json library to convert Python objects to JSON format
import time #import the time library to add delays between sending messages
import random #import the random library to generate random numbers for delays and data generation

fake= Faker() #create an instance of the Faker class to generate fake data

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def generate_fake_pin_result():#define a function that generates a fake pin result using the Faker library
    return {"index": fake.random_int(min=1, max=1000),
            "unique_id": fake.uuid4(),
            "title": fake.sentence(nb_words=6),
            "description": fake.text(max_nb_chars=200),
            "poster_name": fake.name(),
            "follower_count": fake.random_int(min=0, max=10000),
            "tag_list": ",".join([fake.word() for _ in range(5)]),
            "is_image_or_video": fake.random_element(elements=["image", "video"]),
            "image_src": fake.image_url(),
            "downloaded": fake.random_int(min=0, max=1),
            "save_location": fake.file_path(),
            "category": fake.word()}

def generate_fake_geo_result():#define a function that generates a fake geo result using the Faker library
    return {"ind": fake.random_int(min=1, max=1000),
            "timestamp": fake.date_time().isoformat(),
            "latitude": float(fake.latitude()),
            "longitude": float(fake.longitude()),
            "country": fake.country()}

def generate_fake_user_result():#define a function that generates a fake user result using the Faker library
    return {"ind": fake.random_int(min=1, max=1000),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "age": fake.random_int(min=18, max=80),
            "date_joined": fake.date_time().isoformat()}

while True:
    pin_result = generate_fake_pin_result()#generate a fake pin result
    geo_result = generate_fake_geo_result()#generate a fake geo result
    user_result = generate_fake_user_result()#generate a fake user result

    producer.send('pinterest.pin', value=pin_result)#send the fake pin result to the Kafka topic 'pinterest.pin'
    producer.send('pinterest.geo', value=geo_result)#send the fake geo result to the Kafka topic 'pinterest.geo'
    producer.send('pinterest.user', value=user_result)#send the fake user result to the Kafka topic 'pinterest.user'

    print(f"Sent pin: {pin_result['unique_id']}")
    print(f"Sent geo: {geo_result['country']}")
    print(f"Sent user: {user_result['ind']}")
    
    time.sleep(random.uniform(0.5, 2))