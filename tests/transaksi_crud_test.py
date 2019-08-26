import json
from . import app, client, cache, create_token_int, create_token_non, create_token_for_book

class TestTransaksiCrud():

    temp_id = 0

    def test_transaksi_post(self,client):
      token = create_token_for_book()
      inputan = {
            "buku_id" : 4,
            "jumlah" : 1,
            "status" : "keranjang"
        }
      res = client.post('/transaksi', data=json.dumps(inputan),headers={'Authorization' : "Bearer "+token}, content_type='application/json')

      res_json = json.loads(res.data)
      TestTransaksiCrud.temp_id = res_json['id']
      assert res.status_code == 200
    
    def test_transaksi_invalid_post(self,client):
      token=create_token_for_book()
      inputan = {
            "buku_id" : 4,
            "status" : "keranjang"
        }
      res = client.post('/transaksi', data=json.dumps(inputan), headers={'Authorization' : "Bearer "+token},content_type='application/json')

      assert res.status_code == 400

    def test_get_one_invalid(self,client):
      token=create_token_int()
      res = client.get('/transaksi/'+str(TestTransaksiCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 403
    
    def test_transaksi_put(self, client):
      token=create_token_for_book()
      inputan = {
            "status" : "pesan"
        }
      res = client.put('/transaksi/'+str(TestTransaksiCrud.temp_id), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 200
    
    def test_transaksi_invalid_put(self, client):
      token=create_token_int()
      inputan = {
            "status" : "coba aja"
        }
      res = client.put('/transaksi/50000', data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 404
    
    def test_transaksi_admin_put(self, client):
      token=create_token_int()
      inputan = {
            "status" : "terkirim"
        }
      res = client.put('/transaksi/admin/'+str(TestTransaksiCrud.temp_id), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 200

    def test_transaksi_admin_invalid_put(self, client):
      token=create_token_int()
      inputan = {
            "status" : "coba aja"
        }
      res = client.put('/transaksi/50000', data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

      assert res.status_code == 404


    def test_transaksi_delete(self,client):
        token=create_token_for_book()
        res = client.delete('/transaksi/'+str(TestTransaksiCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200

    def test_transaksi_invalid_delete(self,client):
        token=create_token_int()
        res = client.delete('/transaksi/'+str(TestTransaksiCrud.temp_id), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 404

    def test_transaksi_list_private(self, client):
      token = create_token_for_book()
      res = client.get('/transaksi/semua', headers={'Authorization' : "Bearer "+token})

      assert res.status_code == 200
      
    def test_transaksi_list_invalid_token(self, client):
      res = client.get('/transaksi/semua', headers={'Authorization' : "Bearer salah"})

      assert res.status_code == 500
    
    def test_transaksi_get_admin(self, client):
      token = create_token_int()
      res = client.get('/transaksi/admin', headers={'Authorization' : "Bearer "+token})

      assert res.status_code == 200
    
    def test_transaksi_invalid_get_admin(self, client):
      token = create_token_for_book()
      res = client.get('/transaksi/admin', headers={'Authorization' : "Bearer "+token})

      assert res.status_code == 403
    
