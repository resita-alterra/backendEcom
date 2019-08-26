import json
from . import app, client, cache, create_token_int, create_token_non

class TestUserCrud():

    temp_client = 0

    def test_user_list(self, client):
        token = create_token_int()
        res = client.get('/user', headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200
    
    def test_user_list_invalid_token(self, client):
        res = client.get('/user', headers={'Authorization': 'Bearer abc'})
        assert res.status_code == 500

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
    
    def test_user_duplicate_post(self,client):
        token=create_token_int()
        inputan = {
            "user_name" : "userdummy",
            "password" : "fields.Stfdringdfd",
            "alamat" : "fields.fdsStrifdsng",
            "hp" : "fields.Strifdngsdf",
            "email" : "hggf",
            "foto" : "not_show",
            "rekening" : "fieldsdf.Stringdfds"
        }
        res = client.post('/user', data=json.dumps(inputan), content_type='application/json')

        assert res.status_code == 500
    
    def test_user_put(self, client):
        token=create_token_non()
        inputan = {
            "password" : "password",
            "alamat" : "fields.fdsStrifdsng",
            "hp" : "fields.Strifdngsdf",
            "email" : "hggf",
            "foto" : "gantiiii",
            "rekening" : "fieldsdf.Stringdfds"
        }
        res = client.put('/user', data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200
    
    def test_user_invalid_put(self, client):
        token=create_token_int()
        inputan = {
            "password" : "password",
            "alamat" : "fields.fdsStrifdsng",
            "hp" : "fields.Strifdngsdf",
            "email" : "hggf",
            "foto" : "gantiiii",
            "rekening" : "fieldsdf.Stringdfds"
        }
        res = client.put('/user/'+str(TestUserCrud.temp_client), data=json.dumps(inputan), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 500
    
    def test_user_get_me(self,client):
        token= create_token_non()
        res = client.get('/user', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200
        
    def test_user_invalid_get_me(self,client):
        token= create_token_non()
        res = client.get('/user/dsa', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 500

    def test_user_delete(self,client):
        token=create_token_int()
        res = client.delete('/user/'+str(TestUserCrud.temp_client), content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 200

    def test_book_invalid_delete(self,client):
        token=create_token_int()
        res = client.delete('/user/baka', content_type='application/json',headers={'Authorization': 'Bearer '+ token})

        assert res.status_code == 404
