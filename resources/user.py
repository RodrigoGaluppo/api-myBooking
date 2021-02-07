from flask_restful import Resource,reqparse
from models.User import UserModel
from flask_jwt_extended import create_access_token,jwt_required,get_raw_jwt
from werkzeug.security import safe_str_cmp
import traceback
from flask import make_response,render_template

class Users(Resource):

    def post(self):
        arguments = reqparse.RequestParser()
        arguments.add_argument("login",type=str,required=True,help="the filed login is required")
        arguments.add_argument("password",type=str,required=True,help="the filed password is required")
        arguments.add_argument("email",type=str,required=True,help="the filed email is required")
        arguments.add_argument("active",type=bool)

        data = arguments.parse_args()

        if(data.get("email")):
            if(UserModel.find_login(login=data["login"])):
                return {"message":"login already taken"},400

            if(UserModel.find_email(email=data["email"])):
                return {"message":"this email is not available"},400

            new_user = UserModel(**data)
            
            try:
                new_user.active = False
                new_user.save_user()
                new_user.send_confirmation_email()
                return new_user.json(),201
            except:
                new_user.delete_user()
                traceback.print_exc()
                return {"message":"an internal error ocurred when saving data"},500
        else:
             return {"message":"email can not be null"},500

class User(Resource):

    def get(self,user_id):
        user = UserModel.find_user(user_id)

        if user:
            return user.json()
        return {"message":"user not found"},404
 
    def delete(self,user_id):

        user = UserModel.find_user(user_id)
        if(user):
            try:
                user.delete_user()
                return {"message":"user has been removed"},200
            except:
                return {"message":"an internal error ocurred when deleting data"},500

        return {"message":"user not found"},404

class UserLogin(Resource):

    @classmethod
    def post(cls):
        arguments = reqparse.RequestParser()
        arguments.add_argument("login",type=str,required=True,help="the filed login is required")
        arguments.add_argument("password",type=str,required=True,help="the filed password is required")
        arguments.add_argument("email",type=str,required=True,help="the filed email is required")
        arguments.add_argument("active",type=bool)

        data = arguments.parse_args()
        if data.get("email"):
            user = UserModel.find_login(data["login"])
            if user and safe_str_cmp(user.password,data["password"]) and safe_str_cmp(user.email,data["email"]):
                if user.active:
                    acess_token = create_access_token(identity=user.user_id)
                    return {"acess_token":acess_token},200
                else:
                    return {"message":"user is not confirmed"},403
            return {"message":"user not found"},404
        else:
            return {"message":"the field email can not be null"},404

class UserLogout(Resource):
    @jwt_required
    def post(self):
        return {"message","Logged out successfully"},200

class UserConfirm(Resource):
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_user(user_id)
        
        if not user:
            return {"message":"user not found"},404

        user.active = True
        user.save_user()
        headers = {"Content-Type":"text/html"}
        return make_response(render_template("user_confirmed.html",email=user.email,user=user.login),200,headers)

        
        
        