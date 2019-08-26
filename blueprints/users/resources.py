import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import ListUser
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db,app, internal_required


bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):

    def __init__(self):
        pass
    def options(self, id=None):
        return {"ok":"ok"},200
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_name',location='json',required = True)
        parser.add_argument('password',location='json',required = True)
        parser.add_argument('alamat',location='json')
        parser.add_argument('rekening',location='json', required = True)
        parser.add_argument('hp',location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('foto', location='json')

        args = parser.parse_args()
        data = {
            'user_name':args['user_name'],
            'password':args['password'],
            'alamat':args['alamat'],
            'rekening':args['rekening'],
            'hp':args['hp'], 
            'email':args['email'],
            'foto':args['foto']
        }
        user = ListUser(data)
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, ListUser.response_fields), 200, {'Content_Type' : 'application/json'}

    @jwt_required
    def get(self):
        aku= get_jwt_claims()
        
        return aku,200
    
    @internal_required
    def delete(self,id):
        qry = ListUser.query.get(id)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404, {'Content_Type' : 'application/json'}
        
        db.session.delete(qry)
        db.session.commit()

        return {'status' : 'DELETED'}, 200, {'Content_Type' : 'application/json'}

    
    @jwt_required
    def put(self):
        aku= get_jwt_claims()
        parser = reqparse.RequestParser()

        parser.add_argument('password',location='json')
        parser.add_argument('alamat',location='json')
        parser.add_argument('rekening',location='json')
        parser.add_argument('hp',location='json')
        parser.add_argument('email', location='json')
        parser.add_argument('foto', location='json')

        args = parser.parse_args()

        qry = ListUser.query.get(aku['id'])

        if qry is None:
            return { 'status' : 'NOT FOUND'}, 404,{'Content_Type' : 'application/json'}
        
        if args['password'] is not None:
            qry.password = args['password']
        
        if args['alamat'] is not None:
            qry.alamat = args['alamat']
        if args['rekening'] is not None:
            qry.rekening = args['rekening']
        if args['hp'] is not None:
            qry.hp = args['hp']
        if args['email'] is not None:
            qry.email = args['email']
        if args['foto'] is not None:
            qry.foto = args['foto']
        
        db.session.commit()

        return marshal(qry, ListUser.response_fields), 200, {'Content_Type' : 'application/json'}

class AdminUser(Resource):
    def __init__(self):
        pass
    def options(self , id=None):
        return {"ok":"ok"},200
    @internal_required
    def get(self):
        qry = ListUser.query
        hasil = []
        for user in qry:
            data = marshal(user, ListUser.response_fields)
            hasil.append(data)
        
        return hasil, 200 , {'Content_Type' : 'application/json'}
        
    

api.add_resource(UserResource,'','/<id>')
api.add_resource(AdminUser,'/admin')