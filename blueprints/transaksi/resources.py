import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from blueprints import db,app
from sqlalchemy import desc
from .model import DaftarTransaksi
from blueprints.buku.model import DaftarBuku
from blueprints.users.model import ListUser
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import  internal_required

bp_transaksi = Blueprint('transaksi', __name__)
api = Api(bp_transaksi)

class TransaksiResource(Resource):

    def options(self, id=None):
        return {"ok":"ok"},200

    def __init__(self):
        pass
    
    @jwt_required
    def post(self):
        aku = get_jwt_claims()
    
        parser = reqparse.RequestParser()

        parser.add_argument('buku_id', location='json', type=int,required=True)
        parser.add_argument('jumlah', location='json', type=int,required=True)
        parser.add_argument('status', location='json', required=True)

        args = parser.parse_args()

        bukunya = DaftarBuku.query.get(args['buku_id'])

        data_buku = marshal(bukunya, DaftarBuku.response_fields)
        pemilik = ListUser.query.get(data_buku['user_id'])
        data_pemilik = marshal(pemilik, ListUser.response_fields)

        total = data_buku['harga']*args['jumlah']
        
        data = {
            'pembeli_id' : aku['id'], 
            'pembeli_name' : aku['user_name'],
            'penjual_id':data_buku['user_id'], 
            'penjual_name' : data_buku['user_name'],
            'buku_id': args['buku_id'],
            'judul_buku' : data_buku['judul'], 
            'harga_satuan':data_buku['harga'], 
            'jumlah':args['jumlah'], 
            'total_harga':total,
            'alamat_pembeli' : aku['alamat'] ,
            'kontak_pembeli' : aku['hp'],
            'kontak_penjual':data_pemilik['hp'],
            'status': args['status']
        }
        transaksi = DaftarTransaksi(data)

        db.session.add(transaksi)
        db.session.commit()

        app.logger.debug('DEBUG : %s', transaksi)

        return marshal(transaksi, DaftarTransaksi.response_fields), 200, {'Content_Type' : 'application/json'}
    
    
    @jwt_required
    def get(self,id):
        aku = get_jwt_claims()
        qry = DaftarTransaksi.query.get(id)

        if qry is None:
            return {'status' : 'Not Found'}, 404, {'Content_Type' : 'application/json'}
        
        if qry.penjual_id != aku['id']:
            return {'warning' : 'not yours'}, 403, {'Content_Type' : 'application/json'}
        
        hasil = marshal(qry, DaftarTransaksi.response_fields)

        return hasil, 200, {'Content_Type' : 'application/json'}
    
    @jwt_required
    def put(self,id):
        parser = reqparse.RequestParser()

        parser.add_argument('status', location='json')

        args = parser.parse_args()

        qry = DaftarTransaksi.query.get(id)

        if qry is None:
            return { 'status' : 'NOT FOUND'}, 404,{'Content_Type' : 'application/json'}
        
        if args['status'] == 'pesan':
            bukunya=DaftarBuku.query.get(qry.buku_id)
            if bukunya.stok < qry.jumlah:
                return {'status' : 'Buku habis terjual'}, 404, {'Content_Type' : 'application/json' }
        
            bukunya.stok = bukunya.stok - qry.jumlah
                
            qry.status = args['status']
            db.session.commit()

        return marshal(qry, DaftarTransaksi.response_fields), 200,{'Content_Type' : 'application/json'}

    @jwt_required
    def delete(self,id):
        aku = get_jwt_claims()
        qry = DaftarTransaksi.query.get(id)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404, {'Content_Type' : 'application/json'}
        
        if aku['id'] != qry.pembeli_id:
            return {'Warning' : 'Not yours'}, 403, {'Content_Type' : 'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {'status' : 'DELETED'}, 200, {'Content_Type' : 'application/json'}


class TransaksiSemua(Resource):

    def options(self, id=None):
        return {"ok":"ok"},200
    @jwt_required
    def get(self):
        aku = get_jwt_claims()
        as_penjual = DaftarTransaksi.query.filter_by(penjual_id = aku['id'])
        as_pembeli = DaftarTransaksi.query.filter_by(pembeli_id = aku['id'])
        
        penjual = []
        pembeli = []
        keranjang = []

        for i in as_pembeli:
            if i.status != "keranjang":
                tambah = marshal(i, DaftarTransaksi.response_fields)
                pembeli.append(tambah)
            else :
                tambah = marshal(i, DaftarTransaksi.response_fields)
                keranjang.append(tambah)
        for j in as_penjual:
            tambah = marshal(j, DaftarTransaksi.response_fields)
            penjual.append(tambah)

        return {'penjual' : penjual , 'pembeli' : pembeli, 'keranjang': keranjang}, 200, {'Content_Type' : 'application/json'}

class TransaksiAdmin(Resource):
    def __init__(self):
        pass
    def options(self , id=None):
        return {"ok":"ok"},200
    
    @internal_required
    def get(self):
        qry = DaftarTransaksi.query
        hasil = []
        for trx in qry:
            data = marshal(trx, DaftarTransaksi.response_fields)
            hasil.append(data)
        
        return hasil, 200 , {'Content_Type' : 'application/json'}
    
    @internal_required
    def put(self,id):
        parser = reqparse.RequestParser()

        parser.add_argument('status', location='json')

        args = parser.parse_args()

        qry = DaftarTransaksi.query.get(id)

        if qry is None:
            return { 'status' : 'NOT FOUND'}, 404,{'Content_Type' : 'application/json'}
        
        if args['status'] != 'terkirim' or qry.status != 'pesan':
            return {'Warning' : 'Admin hanya bisa mengubah status dari pesan menjadi terkirim'}, 403
                
        qry.status = args['status']
        db.session.commit()

        return marshal(qry, DaftarTransaksi.response_fields), 200,{'Content_Type' : 'application/json'}


api.add_resource(TransaksiResource,'','/<id>')
api.add_resource(TransaksiSemua,'/semua')
api.add_resource(TransaksiAdmin,'/admin','/admin/<id>')