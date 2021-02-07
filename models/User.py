import os
import smtplib
from sql_alchemy import database
from flask import request,url_for
from email.message import EmailMessage

ENDERECO_EMAIL = os.getenv("ENDERECO_EMAIL")
SENHA_EMAIL = os.getenv("SENHA_EMAIL")

class UserModel(database.Model):

    __tablename__ = "users"

    user_id = database.Column(database.Integer,primary_key=True,nullable=False, unique=True, autoincrement=True)
    login = database.Column(database.String(40),nullable=False)
    password = database.Column(database.String(40),nullable=False)
    active= database.Column(database.Boolean,default=False)
    email = database.Column(database.String(80),nullable=False, unique=True)

    def __init__(self,login,password,active,email):
        self.login = login
        self.password = password
        self.email = email
        self.active = active

    def json(self):
        return {
            "user_id":self.user_id,
            "login":self.login,
            "email":self.email,
            "active":self.active
        }
    
    @classmethod
    def find_user(cls,user_id):
        user = cls.query.filter_by(user_id = user_id).first()
        if user:
            return user
        else:
            return None

    @classmethod
    def find_login(cls,login):
        user = cls.query.filter_by(login = login).first()
        if user:
            return user
        else:
            return None

    @classmethod
    def find_email(cls,email):
        user = cls.query.filter_by(email = email).first()
        if user:
            return user
        else:
            return None

    def save_user(self):
        database.session.add(self)
        database.session.commit()

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for("userconfirm",user_id=self.user_id)
        msg = EmailMessage()
        msg["Subject"] = "Email Confirmation"
        msg["From"] = ENDERECO_EMAIL
        msg["To"] = self.email
        content = f"ola {self.login} clique no link {link}"
        msg.set_content(content)
        
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as stmp:
            stmp.login(ENDERECO_EMAIL,SENHA_EMAIL)
            stmp.send_message(msg)

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()
    
    
        