import json
from . import app, client, cache, create_token_int, create_token_non, create_token_for_book, reset_database
from blueprints import db

class TestUserCrud():

    temp_client = 0
    reset_database()


    # 1 test_user_list untuk memastikan hanya admin yang bisa mengakses seluruh data user
    def test_user_list(self, client):
        token = create_token_int()
        res = client.get('/user/admin', headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200
    
    def test_user_list_invalid_token(self, client):
        res = client.get('/user/admin', headers={'Authorization': 'Bearer abc'})
        assert res.status_code == 422
    
    def test_user_list_invalid_user(self, client):
        token = create_token_for_book()
        res = client.get('/user/admin', headers={'Authorization': 'Bearer ' + token})
        assert res.status_code == 403

    # 2 test post user baru
    def test_user_post(self,client):
        inputan = {
            "user_name" : "userdummy",
            "password" : "password",
            "rekening" : "fields.fdsStrifdsng",
            "hp" : "fields.Strifdngsdf",
            "alamat" : "jsdhsgd",
            "email" : "not_show",
            "foto" : "fieldsdf.Stringdfds"
        }
        res = client.post('/user', data=json.dumps(inputan), content_type='application/json')

        res_json = json.loads(res.data)
        TestUserCrud.temp_client = res_json['id']
        assert res.status_code == 200
    
    # def test_user_post_duplicate(self,client):
        # 
        # inputan = {
            # "user_name" : "userdummy",
            # "password" : "fields.Stfdringdfd",
            # "alamat" : "fields.fdsStrifdsng",
            # "hp" : "fields.Strifdngsdf",
            # "email" : "hggf",
            # "foto" : "not_show",
            # "rekening" : "fieldsdf.Stringdfds"
        # }
        # res = client.post('/user', data=json.dumps(inputan), content_type='application/json')
# 
        # assert res.status_code == 500
    
    def test_user_post_unfilled_required(self,client):
        inputan = {
            "user_name" : "userdummy2",
            "password" : "fields.Stfdringdfd",
            "rekening" : "fieldsdf.Stringdfds"
        }
        res = client.post('/user', data=json.dumps(inputan), content_type='application/json')

        assert res.status_code == 400        

    # 3 test put user dummy
    def test_user_put(self, client):
        token=create_token_non()
        inputan = {
            "password" : "password",
            "alamat" : "ganti",
            "hp" : "ganti",
            "email" : "ganti",
            "foto" : "gantiiii",
            "rekening" : "ganti"
        }
        res = client.put('/user', data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200
    
    # assert 500 karena user admin(token int) mencoba mengubah data user yang bukan dirinya
    # def test_user_put_invalid_user(self, client):
    #     token=create_token_int()
    #     inputan = {
    #         "password" : "password",
    #         "alamat" : "fields.fdsStrifdsng",
    #         "hp" : "fields.Strifdngsdf",
    #         "email" : "hggf",
    #         "foto" : "gantiiii",
    #         "rekening" : "fieldsdf.Stringdfds"
    #     }
    #     res = client.put('/user/'+str(TestUserCrud.temp_client), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

    #     assert res.status_code == 500
    
    # 4 test mendapatkan data pribadi user
    def test_user_get_me(self,client):
        token= create_token_non()
        res = client.get('/user', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200
        
    # def test_user_get_me_invalid_id(self,client):
    #     token= create_token_non()
    #     res = client.get('/user/dsa', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

    #     assert res.status_code == 500

    # 5 test menghapus user
    def test_user_delete_invalid_admin(self,client):
        token=create_token_for_book()
        res = client.delete('/user/'+str(TestUserCrud.temp_client), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 403

    def test_user_delete(self,client):
        token=create_token_int()
        res = client.delete('/user/'+str(TestUserCrud.temp_client), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200

    def test_user_delete_invalid_id(self,client):
        token=create_token_int()
        res = client.delete('/user/baka', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 404

    def test_user_option(self,client):
      res = client.options('/user',content_type='application/json')

      assert res.status_code == 200

    def test_user_admin_option(self,client):
      res = client.options('/user/admin',content_type='application/json')

      assert res.status_code == 200