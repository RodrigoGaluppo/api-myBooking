from os import getenv
from flask import Flask
from flask_restful import Api
from resources.hotel import Hotels,Hotel
from resources.user import Users,User,UserLogin,UserLogout,UserConfirm
from resources.site import Site,Sites
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = (60*60*24*30)
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_database():
    database.create_all()

api.add_resource(Hotels,"/hotels")
api.add_resource(Hotel,"/hotels/<int:hotel_id>")
api.add_resource(Users,"/users")
api.add_resource(User,"/users/<int:user_id>")
api.add_resource(UserLogin,"/login")
api.add_resource(Sites,"/sites")
api.add_resource(Site,"/sites/<string:url>")
api.add_resource(UserConfirm,"/confirmation/<int:user_id>")

if __name__ == "__main__":
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)