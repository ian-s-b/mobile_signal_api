"""File containing the Signal API for Sites Mobiles."""
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
from unidecode import unidecode
from utils.api_adresse import ApiAdresse
from utils.create_logger import CreateLogger
from logging import ERROR


logger = CreateLogger("signal_api", ERROR).get_logger()

# API initialization and database connection
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/'
mongo_client = MongoClient(app.config['MONGO_URI'])
database = mongo_client.sites_mobiles
collection = database.city_signal

api = Api(app)

# Object used to make requests to the "API Adresse"
api_adresse = ApiAdresse(logger)

class SignalDataResource(Resource):
    """Methods to be used on the city_signal document from sites_mobiles database."""
    def get(self):
        """Get signal data method."""
        address = request.args.get('q')

        response = api_adresse.search(query=address, timeout=10)

        response_len = len(response["features"])

        if response_len == 0:
            return {"message": "The requested address was not found."}, 404

        results = {}
        for features in response["features"]:
            city_code = str(features["properties"]["citycode"])
            city_name = str(features["properties"]["city"])
            city_key = unidecode(f"{city_code} {city_name}")

            if city_code:
                signal_mobile = collection.find_one({"city_code": city_code})

                if signal_mobile:
                    results[city_key] = signal_mobile["signal_data"]

                else:
                    results[city_key] = {'message': f'city_code {city_code} not found in the database'}

        if results:
            return jsonify(results)
        
        return {'message': 'address {address} not found with the API Adresse.'}, 404

# Make the resources available on the API on the endpoint '/'
api.add_resource(SignalDataResource, '/')
