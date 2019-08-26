import json
from . import app, client, cache, create_token_int, create_token_non, create_token_for_book

class TestBookCrud():

    temp_id = 0

    def test_book_list(self, client):
      token = create_token_for_book()
      res = client.get('/bacaan', headers={'Authorization' : "Bearer "+token})

      assert res.status_code == 200
      
    def test_book_list_invalid_token(self, client):
      token = create_token_for_book()
      res = client.get('/bacaan', headers={'Authorization' : "Bearer jasa"})

      assert res.status_code == 500
    
    def test_book_list_publik(self, client):
      token = create_token_for_book()
      res = client.get('/bacaan/publik')

      assert res.status_code == 200

    def test_book_post(self,client):
      token = create_token_for_book()
      inputan = {
            "judul" : "Conan",
            "pengarang" : "Aoyama Gosho",
            "penerbit" : "Gramedia",
            "harga" : 50000,
            "stok" : 2,
            "url_picture" : "https://upload.wikimedia.org/wikipedia/commons/7/77/Sherlock_Holmes_%26_Watson_-_The_Greek_Interpreter_-_Sidney_Paget.jpg",
            "deskripsi" : "ngasal",
            "tipe" : "komik"
        }
      res = client.post('/bacaan', data=json.dumps(inputan),headers={'Authorization' : "Bearer "+token}, content_type='application/json')

      res_json = json.loads(res.data)
      TestBookCrud.temp_id = res_json['id']
      assert res.status_code == 200
    
    def test_book_invalid_post(self,client):
      token=create_token_for_book()
      inputan = {
            "judul" : "userdummy"
        }
      res = client.post('/bacaan', data=json.dumps(inputan), content_type='application/json')

      assert res.status_code == 500
    
    def test_book_put(self, client):
      token=create_token_for_book()
      inputan = {
            "judul" : "Conan",
            "pengarang" : "Aoyama Gosho",
            "penerbit" : "Gramedia",
            "harga" : 50000,
            "stok" : 2,
            "url_picture" : "https://upload.wikimedia.org/wikipedia/commons/7/77/Sherlock_Holmes_%26_Watson_-_The_Greek_Interpreter_-_Sidney_Paget.jpg",
            "deskripsi" : "gantiiii"
        }
      res = client.put('/bacaan/'+str(TestBookCrud.temp_id), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 200
    
    def test_book_invalid_put(self, client):
      token=create_token_int()
      inputan = {
            "judul" : "Conan",
            "pengarang" : "Aoyama Gosho",
            "penerbit" : "Gramedia",
            "harga" : 50000,
            "stok" : 2,
            "url_picture" : "https://upload.wikimedia.org/wikipedia/commons/7/77/Sherlock_Holmes_%26_Watson_-_The_Greek_Interpreter_-_Sidney_Paget.jpg",
            "deskripsi" : "ngasal"
        }
      res = client.put('/bacaan/'+str(TestBookCrud.temp_id), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 403
    
    def test_get_one(self,client):
      token=create_token_for_book()
      res = client.get('/bacaan/'+str(TestBookCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 200
    def test_get_one_invalid(self,client):
      token=create_token_for_book()
      res = client.get('/bacaan/0', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 404
      

    def test_book_delete(self,client):
        token=create_token_for_book()
        res = client.delete('/bacaan/'+str(TestBookCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200

    def test_book_invalid_delete(self,client):
        token=create_token_int()
        res = client.delete('/bacaan/'+str(TestBookCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 404
