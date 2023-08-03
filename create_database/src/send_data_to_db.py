"""Script used to create the signal_api database."""
import json
from pymongo import MongoClient, ASCENDING


# Load json file data
with open("db_data.json", "r", encoding="utf-8") as json_file:
    signal_list = json.load(json_file)

# Database initialization and data injection
client = MongoClient("mongodb://db:27017/")
database = client.sites_mobiles
collection = database.city_signal
collection.create_index([('city_code', ASCENDING)], unique=True)
collection.insert_many(signal_list)

client.close()
