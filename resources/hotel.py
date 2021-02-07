from flask_restful import Resource,reqparse
from models.Hotel import HotelModel
from models.Site import SiteModel
from flask_jwt_extended import jwt_required
from resources.filters import normalize_path_params,query_if_city,query_if_not_city
import sqlite3

path_params = reqparse.RequestParser()
path_params.add_argument("city",type=str)
path_params.add_argument("min_stars",type=float)
path_params.add_argument("max_stars",type=float)
path_params.add_argument("min_price",type=float)
path_params.add_argument("max_price",type=float)
path_params.add_argument("limit",type=float)
path_params.add_argument("offset",type=float)

class Hotels(Resource):
    def get(self):

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        
        data = path_params.parse_args()

        data_validator = { key:data[key] for key in data if data[key] is not None }

        params = normalize_path_params(**data_validator)
 
        if not params.get("city"):
            query = query_if_not_city

            listOfValues = tuple([params[key] for key in params])
            result = cursor.execute(query,listOfValues)
        else:
            query = query_if_city

            listOfValues = tuple([params[key] for key in params])
            result = cursor.execute(query,listOfValues)

        hotels = []
        for line in result:
            hotels.append({
                'hotel_id':line[0],
                'name':line[1],
                'stars':line[2],
                'price':line[3],
                'city':line[4],
                'site_id':line[5],
            })

        return {'hotels':hotels}

    @jwt_required
    def post(self):
        arguments = reqparse.RequestParser()
        arguments.add_argument("name",type=str,required=True,help="the filed name is required")
        arguments.add_argument("stars",type=float,required=True,help="the filed stars is required")
        arguments.add_argument("price",type=float,required=True,help="the filed price is required")
        arguments.add_argument("city",type=str,required=True,help="the filed city is required")
        arguments.add_argument("site_id",type=str,required=True,help="the filed site_id is required")

        data = arguments.parse_args()
        new_hotel = HotelModel(**data)
        
        if not SiteModel.find_by_id(data.get("site_id")):
            return {"message":"the hotel must be associated with a valid site"},400
        else:
            try:
                new_hotel.save_hotel()
                return new_hotel.json(),201
            except:
                return {"message":"an internal error ocurred when saving data"},500

class Hotel(Resource):

    def get(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            return hotel.json()
        return {"message":"hotel not found"},404
    
    @jwt_required
    def put(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if(hotel):
            arguments = reqparse.RequestParser()
            arguments.add_argument("name")
            arguments.add_argument("stars")
            arguments.add_argument("price")
            arguments.add_argument("city")

            data = arguments.parse_args()

            hotel.update_hotel(**data)
            
            try:
                new_hotel.save_hotel()
                return hotel.json()
            except:
                return {"message":"an internal error ocurred when saving data"},500

        return {"message":"hotel not found"},404

    @jwt_required
    def delete(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if(hotel):
            try:
                hotel.delete_hotel()
                return {"message":"hotel has been removed"},200
            except:
                return {"message":"an internal error ocurred when deleting data"},500

        return {"message":"hotel not found"},404
        
        