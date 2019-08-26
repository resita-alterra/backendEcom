from blueprints import db
from flask_restful import fields

class DaftarBuku(db.Model):
    __tablename__ = "buku"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    judul = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.String(1000), nullable=True)
    pengarang = db.Column(db.String(100), nullable = True)
    penerbit = db.Column(db.String(100), nullable = True)
    harga = db.Column(db.Integer, nullable=False)
    stok = db.Column(db.Integer, nullable=False)
    tipe = db.Column(db.String(10), nullable=False)
    url_picture = db.Column(db.String(300), default = "https://image.flaticon.com/icons/png/512/130/130304.png")

    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'user_name' : fields.String,
        'judul' : fields.String,
        'deskripsi' : fields.String,
        'pengarang' : fields.String,
        'penerbit' : fields.String,
        'harga' : fields.Integer,
        'stok' : fields.Integer,
        'tipe' : fields.String,
        'url_picture' : fields.String
    }
    
    def __init__(self,data):
        self.user_id = data['user_id']
        self.user_name = data['user_name']
        self.judul = data['judul']
        self.deskripsi = data['deskripsi']
        self.pengarang = data['pengarang']
        self.penerbit = data['penerbit']
        self.harga = data['harga']
        self.stok = data['stok']
        self.tipe = data['tipe']
        self.url_picture = data['url_picture']
    
    def __repr__(self):
        return '<Buku %r>' % self.id