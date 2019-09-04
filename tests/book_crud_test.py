import json
from . import app, client, cache, create_token_int, create_token_non, create_token_for_book, create_token_for_book_2, reset_database

class TestBookCrud():

    temp_id = 0
    reset_database()

    # 1 test mendapatkan list buku pribadi
    def test_book_list(self, client):
      token = create_token_for_book()
      res = client.get('/bacaan', headers={'Authorization' : "Bearer "+token})

      assert res.status_code == 200
      
    def test_book_list_invalid_token(self, client):
      token = create_token_for_book()
      res = client.get('/bacaan', headers={'Authorization' : "Bearer ngasal"})

      assert res.status_code == 422

    # 2 test mendapatkan list seluruh buku
    def test_book_list_publik(self, client):

      data = {
        "tipe" : "komik",
        "order" : "harga"
      }
      
      res = client.get('/bacaan/publik', query_string=data)

      assert res.status_code == 200


    # 3 test post buku baru
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
    
    def test_book_post_unfilled_required(self,client):
      token=create_token_for_book()
      inputan = {
            "judul" : "userdummy"
        }
      res = client.post('/bacaan', data=json.dumps(inputan), headers={'Authorization' : "Bearer "+token}, content_type='application/json')

      assert res.status_code == 400
    
    # 4 test ubah data buku
    def test_book_put(self, client):
      token=create_token_for_book()
      inputan = {
            "judul" : "ganti",
            "pengarang" : "ganti",
            "penerbit" : "ganti",
            "harga" : 50000,
            "tipe" : "novel",
            "stok" : 2,
            "url_picture" : "https://upload.wikimedia.org/wikipedia/commons/7/77/Sherlock_Holmes_%26_Watson_-_The_Greek_Interpreter_-_Sidney_Paget.jpg",
            "deskripsi" : "gantiiii"
        }
      res = client.put('/bacaan/'+str(TestBookCrud.temp_id), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 200
    
    def test_book_put_invalid_user(self, client):
      token=create_token_for_book_2()
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

    def test_book_put_invalid_id(self, client):
      token=create_token_for_book_2()
      inputan = {
            "judul" : "Conan",
            "pengarang" : "Aoyama Gosho",
            "penerbit" : "Gramedia",
            "harga" : 50000,
            "stok" : 2,
            "url_picture" : "https://upload.wikimedia.org/wikipedia/commons/7/77/Sherlock_Holmes_%26_Watson_-_The_Greek_Interpreter_-_Sidney_Paget.jpg",
            "deskripsi" : "ngasal"
        }
      res = client.put('/bacaan/id', data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 404  
    
    # 5 test mendapatkan satu buku spesifik 
    def test_get_one(self,client):
      res = client.get('/bacaan/'+str(TestBookCrud.temp_id), content_type='application/json')

      assert res.status_code == 200

    def test_get_one_invalid_id(self,client):
      token=create_token_for_book()
      res = client.get('/bacaan/0', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 404

    # 6 test menghapus buku

    def test_book_delete_invalid_user(self,client):
        token=create_token_for_book_2()
        res = client.delete('/bacaan/'+str(TestBookCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 403

    def test_book_delete(self,client):
        token=create_token_for_book()
        res = client.delete('/bacaan/'+str(TestBookCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200

    def test_book_delete_invalid_id(self,client):
        token=create_token_int()
        res = client.delete('/bacaan/'+str(TestBookCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 404
    
    def test_book_option(self,client):
      res = client.options('/bacaan/2',content_type='application/json')

      assert res.status_code == 200
    
    def test_book_personal_option(self,client):
      res = client.options('/bacaan',content_type='application/json')

      assert res.status_code == 200
    
    def test_publik_book_option(self,client):
      res = client.options('/bacaan/publik',content_type='application/json')

      assert res.status_code == 200
