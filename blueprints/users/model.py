from blueprints import db
from flask_restful import fields
import datetime


class ListUser(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_name = db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    alamat = db.Column(db.String(225), nullable=False)
    rekening = db.Column(db.String(30), nullable=False)
    hp = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    foto = db.Column(db.String(
        300), default="https://cdn1.iconfinder.com/data/icons/main-ui-elements-with-colour-bg/512/male_avatar-512.png")

    response_fields = {
        'id': fields.Integer,
        'user_name': fields.String,
        'password': fields.String,
        'alamat': fields.String,
        'rekening': fields.String,
        'hp': fields.String,
        'email': fields.String,
        'foto': fields.String
    }

    def __init__(self, data):
        self.user_name = data['user_name']
        self.password = data['password']
        self.alamat = data['alamat']
        self.rekening = data['rekening']
        self.hp = data['hp']
        self.email = data['email']
        self.foto = data['foto']

    # def __repr__(self):
        # return '<Person %r>' % self.id
