from flask import Blueprint
from flask_restful import Resource, reqparse, Api
import requests, json
from flask_jwt_extended import jwt_required

bp_weather = Blueprint('weather', __name__)
api = Api(bp_weather)

class CurrentWeather(Resource):
    

    def get(self):
        parser = reqparse.RequestParser()
        wio_host = 'https://api.weatherbit.io/v2.0'
        wio_apikey = '8ff848ce99ae430c9e18ad16cd13754d'

        rq = requests.get(wio_host + '/current?', params={'city': 'Malang,ID', 'key': wio_apikey})
        geo = rq.json()
        return {'temp': geo['data'][0]['temp']},200

api.add_resource(CurrentWeather, '')