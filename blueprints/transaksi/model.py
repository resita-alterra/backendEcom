from blueprints import db
from flask_restful import fields

class DaftarTransaksi(db.Model):

    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key = True)
    pembeli_id = db.Column(db.Integer, nullable= False)
    pembeli_name = db.Column(db.String(100), nullable=False)
    penjual_id = db.Column(db.Integer, nullable= False)
    penjual_name = db.Column(db.String(100), nullable=False)
    buku_id = db.Column(db.Integer, nullable= False)
    judul_buku = db.Column(db.String(200), nullable=False)
    harga_satuan = db.Column(db.Integer, nullable= False)
    jumlah = db.Column(db.Integer, nullable= False)
    total_harga = db.Column(db.Integer, nullable= False)
    alamat_pembeli = db.Column(db.String(300), nullable=False)
    kontak_penjual = db.Column(db.String(100), nullable=False)
    kontak_pembeli = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(40), nullable= False)

    response_fields = {
        'id' : fields.Integer,
        'pembeli_id' : fields.Integer,
        'pembeli_name' : fields.String,
        'penjual_id' : fields.Integer,
        'penjual_name' : fields.String,
        'buku_id' : fields.Integer,
        'judul_buku' : fields.String,
        'harga_satuan' : fields.Integer,
        'jumlah' : fields.Integer,
        'total_harga' : fields.Integer,
        'alamat_pembeli' : fields.String,
        'kontak_penjual' : fields.String,
        'kontak_pembeli' : fields.String,
        'status' : fields.String
    }

    def __init__(self,data):

        self.pembeli_id = data['pembeli_id']
        self.pembeli_name = data['pembeli_name']
        self.penjual_id = data['penjual_id']
        self.penjual_name = data['penjual_name']
        self.buku_id = data['buku_id']
        self.judul_buku = data['judul_buku']
        self.harga_satuan = data['harga_satuan']
        self.jumlah = data['jumlah']
        self.total_harga = data['total_harga']
        self.alamat_pembeli = data['alamat_pembeli']
        self.kontak_pembeli = data['kontak_pembeli']
        self.kontak_penjual = data['kontak_penjual']
        self.status = data['status']
    
    def __repr__(self):
        return '<Transaksi %r>' % self.id