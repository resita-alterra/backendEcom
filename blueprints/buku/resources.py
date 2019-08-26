import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from sqlalchemy import desc
from .model import DaftarBuku
from blueprints import db,app
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_bacaan = Blueprint('bacaan', __name__)
api = Api(bp_bacaan)

class BacaanResource(Resource):

    def __init__(self):
        pass
    
    def options(self, id=None):
        return {"ok":"ok"},200

    @jwt_required    
    def post(self):
        aku= get_jwt_claims()
        parser = reqparse.RequestParser()

        parser.add_argument('judul',location='json', required = True)
        parser.add_argument('deskripsi', location='json')
        parser.add_argument('pengarang',location='json')
        parser.add_argument('penerbit',location='json')
        parser.add_argument('harga',location='json', type=int, required = True)
        parser.add_argument('stok',location='json', type=int, required = True)
        parser.add_argument('tipe', location='json', required=True, choices=('komik','novel','pelajaran','sejarah','agama','umum'))
        parser.add_argument('url_picture',location='json')

        args= parser.parse_args()

        data = {
            'user_id' : int(aku['id']),
            'user_name' : aku['user_name'],
            'judul' : args['judul'],
            'deskripsi' : args['deskripsi'],
            'pengarang' : args['pengarang'],
            'penerbit' : args['penerbit'],
            'harga' : args['harga'],
            'stok' : args['stok'],
            'tipe' : args['tipe'],
            'url_picture' : args['url_picture']

        }
        buku = DaftarBuku(data)

        db.session.add(buku)
        db.session.commit()

        app.logger.debug('DEBUG : %s', buku)

        return marshal(buku, DaftarBuku.response_fields), 200, {'Content_Type' : 'application/json'}
    
    @jwt_required
    def put(self,id):
        aku = get_jwt_claims()
        parser = reqparse.RequestParser()

        parser.add_argument('judul', location='json', nullable= True)
        parser.add_argument('deskripsi', location='json')
        parser.add_argument('pengarang', location='json', nullable= True)
        parser.add_argument('penerbit', location='json', nullable= True)
        parser.add_argument('harga', location='json', type=int, nullable= True)
        parser.add_argument('stok', location='json', type=int , nullable= True)
        parser.add_argument('tipe', location = 'json', choices=('komik','novel','pelajaran','sejarah','agama','umum', None), nullable= True)
        parser.add_argument('url_picture', location='json', nullable= True)

        args = parser.parse_args()
        qry = DaftarBuku.query.get(id)

        if qry is None:
            return {'status' : 'NOT FOUND'}, 404, {'Content_Type' : 'application/json'}
        
        
        if qry.user_id != aku['id']:
            return {'Warning' : 'Not yours'}, 403, {'Content_Type' : 'application/json'}

        if args['judul'] is not None:
            qry.judul = args['judul']
        if args['deskripsi'] is not None:
            qry.deskripsi = args['deskripsi']
        if args['pengarang'] is not None:
            qry.pengarang = args['pengarang']
        if args['penerbit'] is not None:
            qry.penerbit = args['penerbit']
        if args['harga'] is not None:
            qry.harga = args['harga']
        if args['stok'] is not None:
            qry.stok = args['stok']
        if args['tipe'] is not None:
            qry.tipe = args['tipe']
        if args['url_picture'] is not None:
            qry.url_picture = args['url_picture']
        
        db.session.commit()

        return marshal(qry, DaftarBuku.response_fields), 200, {'Content_Type' : 'application/json'}

    @jwt_required
    def delete(self,id):
        aku = get_jwt_claims()
        qry = DaftarBuku.query.get(id)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404, {'Content_Type' : 'application/json'}
        
        if aku['id'] != qry.user_id:
            return {'Warning' : 'Not yours'}, 403, {'Content_Type' : 'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {'status' : 'DELETED'}, 200, {'Content_Type' : 'application/json'}
    
    def get(self,id):
        qry = DaftarBuku.query.get(id)

        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404, {'Content_Type' : 'application/json'}
        
        hasil = marshal(qry, DaftarBuku.response_fields)

        return hasil, 200, {'Content_Type' : 'application/json'}

class BacaanSemuaPersonal(Resource):

    def options(self, id=None):
        return {"ok":"ok"},200

    @jwt_required
    def get(self):
        aku = get_jwt_claims()

        qry = DaftarBuku.query.filter_by(user_id = aku['id'])

        hasil = []
        for buku in qry:
            data = marshal(buku, DaftarBuku.response_fields)
            hasil.append(data)
        
        return hasil, 200 , {'Content_Type' : 'application/json'}

class BacaanSemuaPublic(Resource):

    def options(self, id=None):
        return {"ok":"ok"},200

    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tipe', location='args', choices=('komik','novel','pelajaran','sejarah','agama','umum'))
        parser.add_argument('order', location='args', choices=('stok','harga','judul'))
        qry = DaftarBuku.query

        args = parser.parse_args()

        if args['tipe'] is not None:
            qry = qry.filter_by(tipe=args['tipe'])
        if args['order'] is not None:
            qry = qry.order_by(args['order'])

        hasil = []
        for buku in qry:
            data = marshal(buku, DaftarBuku.response_fields)
            hasil.append(data)
        
        return hasil, 200 , {'Content_Type' : 'application/json'}


api.add_resource(BacaanSemuaPersonal,'')
api.add_resource(BacaanResource,'', '/<id>')
api.add_resource(BacaanSemuaPublic,'/publik')