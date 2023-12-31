"""Script used to create the signal_api database."""
from pathlib import Path
from pymongo import MongoClient, ASCENDING
from logging import ERROR
from utils.csv_parser import SitesMobileCsvConverter
from utils.create_logger import CreateLogger


# Create the logger object
create_database_logger = CreateLogger(app_name='create_database', logger_level=ERROR).get_logger()

# Parse the input csv file:
csv_converter = SitesMobileCsvConverter(
    mobile_csv_path=Path("2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv"),
    logger=create_database_logger,
    separator=";")

# Make the input file to request the 'Api Adresse'
input_file = csv_converter.save_input_csv()

# Make the request and get the response in an output file
output_file = csv_converter.save_adresse_request_csv(input_file)

# Convert the response into a list that can be injectect into the database
signal_list = csv_converter.convert_csv_to_dict(output_file)

# Database initialization and data injection
client = MongoClient("mongodb://localhost:27017/")
database = client.sites_mobiles
collection = database.city_signal
collection.create_index([('city_code', ASCENDING)], unique=True)
collection.insert_many(signal_list)
