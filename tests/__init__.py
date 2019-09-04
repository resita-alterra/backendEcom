import pytest, json, logging
from flask import Flask, request

from blueprints import app, db
from blueprints.users.model import ListUser
from blueprints.buku.model import DaftarBuku
from app import cache

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)
# buat admin
def create_token_int():
    token = cache.get('test-token-int')
    if token is None:
        data = {
            'user_name' : 'admin',
            'password' : 'password'
        }
        # do request
        req = call_client(request)
        res = req.get('/login', query_string=data,content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json )
        assert res.status_code == 200

        cache.set('test_token-int',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token

# token_non akan digunakan untuk testing user dummy(yang pada akhirnya akan dihapus)
def create_token_non():
    token = cache.get('test-token-non')
    if token is None:
        data = {
            'user_name' : 'userdummy',
            'password' : 'password'
        }
        
        req = call_client(request)
        res = req.get('/login', query_string=data,content_type='application/json')

        
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json )
        
        assert res.status_code == 200

        
        cache.set('test_token-non',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token

# token berikut menggunakan user asli
# digunakan utamanya untuk testing book(beberapa method harus menggunakan bearer token)
# digunakan pula untuk testing transaksi dan beberapa yang lain
def create_token_for_book():
    token = cache.get('test-token-for-book')
    if token is None:
        data = {
            'user_name' : 'alzimnae',
            'password' : 'password'
        }
        
        req = call_client(request)
        res = req.get('/login', query_string=data,content_type='application/json')

        
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json )
        
        assert res.status_code == 200

        
        cache.set('test_token-for-book',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token

def create_token_for_book_2():
    token = cache.get('test-token-for-book-2')
    if token is None:
        data = {
            'user_name' : 'tabipo',
            'password' : 'password'
        }
        
        req = call_client(request)
        res = req.get('/login', query_string=data,content_type='application/json')

        
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json )
        
        assert res.status_code == 200

        
        cache.set('test_token-for-book',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token


def reset_database():
    db.drop_all()
    db.create_all()
    admin = {
            'user_name': 'admin',
            'password': 'password',
            'alamat':'jahgad',
            'rekening':'kjashad',
            'hp':'jdh', 
            'email':'inga',
            'foto':'adhag'
        }
    
    user_1 = {
            'user_name': 'alzimnae',
            'password': 'password',
            'alamat':'jahgad',
            'rekening':'kjashad',
            'hp':'jdh', 
            'email':'inga',
            'foto':'adhag'
    }

    user_2 = {
            'user_name': 'tabipo',
            'password': 'password',
            'alamat':'jahgad',
            'rekening':'kjashad',
            'hp':'jdh', 
            'email':'inga',
            'foto':'adhag'
    }
    buku = {
            "user_id" : 2,
            "user_name" : "alzimnae",
            "judul" : "Conan",
            "pengarang" : "Aoyama Gosho",
            "penerbit" : "Gramedia",
            "harga" : 50000,
            "stok" : 100,
            "url_picture" : "https://upload.wikimedia.org/wikipedia/commons/7/77/Sherlock_Holmes_%26_Watson_-_The_Greek_Interpreter_-_Sidney_Paget.jpg",
            "deskripsi" : "ngasal",
            "tipe" : "komik"
        }
    admin = ListUser(admin)
    user_1 = ListUser(user_1)
    user_2 = ListUser(user_2)
    buku = DaftarBuku(buku)
    db.session.add(buku)
    db.session.add(admin)
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()