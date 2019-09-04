import json
from . import app, client, cache, create_token_int, create_token_non, create_token_for_book, create_token_for_book_2, reset_database

class TestTransaksiCrud():

    temp_id = 0
    reset_database()
    # 1 test post transaksi baru
    def test_transaksi_post(self,client):
      token = create_token_for_book()
      inputan = {
            "buku_id" : 1,
            "jumlah" : 1,
            "status" : "keranjang"
        }
      res = client.post('/transaksi', data=json.dumps(inputan),headers={'Authorization' : "Bearer "+token}, content_type='application/json')

      res_json = json.loads(res.data)
      TestTransaksiCrud.temp_id = res_json['id']
      assert res.status_code == 200
    
    def test_transaksi_post_unfilled_required(self,client):
      token=create_token_for_book()
      inputan = {
            "buku_id" : 7,
            "status" : "keranjang"
        }
      res = client.post('/transaksi', data=json.dumps(inputan), headers={'Authorization' : "Bearer "+token},content_type='application/json')

      assert res.status_code == 400
  
    # 2 mendapatkan data transaksi
    def test_get_one_invalid_user(self,client):
      token=create_token_int()
      res = client.get('/transaksi/'+str(TestTransaksiCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 403
    
    def test_get_one_sukses(self,client):
      token=create_token_for_book()
      res = client.get('/transaksi/'+str(TestTransaksiCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 200

    def test_get_one_invalid_id(self,client):
      token=create_token_for_book()
      res = client.get('/transaksi/90', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 404
    
    # 3 mengubah data transaksi
    def test_transaksi_put(self, client):
      token=create_token_for_book()
      inputan = {
            "status" : "pesan"
        }
      res = client.put('/transaksi/'+str(TestTransaksiCrud.temp_id), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 200
    
    def test_transaksi_put_not_found(self, client):
      token=create_token_int()
      inputan = {
            "status" : "coba aja"
        }
      res = client.put('/transaksi/50000', data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 404
    
    def test_transaksi_put_admin(self, client):
      token=create_token_int()
      inputan = {
            "status" : "terkirim"
        }
      res = client.put('/transaksi/admin/'+str(TestTransaksiCrud.temp_id), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 200

    def test_transaksi_put_admin_invalid_status(self, client):
      token=create_token_int()
      inputan = {
            "status" : "coba aja"
        }
      res = client.put('/transaksi/admin/'+str(TestTransaksiCrud.temp_id), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 403

    def test_transaksi_put_admin_invalid_id(self, client):
      token=create_token_int()
      inputan = {
            "status" : "coba aja"
        }
      res = client.put('/transaksi/admin/id', data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 404


    # 5 test mendapatkan list transaksi pribadi
    def test_transaksi_list_private(self, client):
      token = create_token_for_book()
      res = client.get('/transaksi/semua', headers={'Authorization' : "Bearer "+token})

      assert res.status_code == 200
      
    def test_transaksi_list_invalid_token(self, client):
      res = client.get('/transaksi/semua', headers={'Authorization' : "Bearer salah"})

      assert res.status_code == 422
    
    def test_transaksi_get_admin(self, client):
      token = create_token_int()
      res = client.get('/transaksi/admin', headers={'Authorization' : "Bearer "+token})

      assert res.status_code == 200
    
    def test_transaksi_invalid_get_admin(self, client):
      token = create_token_for_book()
      res = client.get('/transaksi/admin', headers={'Authorization' : "Bearer "+token})

      assert res.status_code == 403

    def test_transaksi_option(self,client):
      res = client.options('/transaksi',content_type='application/json')

      assert res.status_code == 200

    def test_transaksi_semua_option(self,client):
      res = client.options('/transaksi/semua',content_type='application/json')

      assert res.status_code == 200

    def test_transaksi_admin_option(self,client):
      res = client.options('/transaksi/admin',content_type='application/json')

      assert res.status_code == 200

    # 4 menghapus transaksi

    def test_transaksi_delete_invalid_user(self,client):
        token=create_token_for_book_2()
        res = client.delete('/transaksi/'+str(TestTransaksiCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 403

    def test_transaksi_delete(self,client):
        token=create_token_for_book()
        res = client.delete('/transaksi/'+str(TestTransaksiCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200

    def test_transaksi_delete_invalid_id(self,client):
        token=create_token_int()
        res = client.delete('/transaksi/'+str(TestTransaksiCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 404

