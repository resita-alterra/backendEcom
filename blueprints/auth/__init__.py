from flask import Blueprint
from blueprints import db,app
from flask_restful import Api, Resource, reqparse, marshal
from blueprints.users.model import ListUser

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_auth = Blueprint('auth',__name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):

    def options(self):
        return {"ok":"ok"},200

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('user_name', location='args')
        parser.add_argument('password', location='args')

        args = parser.parse_args()
        qry = ListUser.query.filter_by(user_name=args['user_name']).filter_by(password=args['password'])


        if qry.count()>0:
            akun=qry.first()
            akun=marshal(akun,ListUser.response_fields)
            akun.pop('password')
            token=create_access_token(identity=args['user_name'],user_claims=akun)
            return {'token': token},200
        else:
            return {'status': 'UNAUTHORIZED'},401

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        return {'claims' : claims}, 200

class RefreshTokenResource(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user)
        return {'token':token},200

api.add_resource(CreateTokenResource,'')
api.add_resource(RefreshTokenResource,'/refresh')
