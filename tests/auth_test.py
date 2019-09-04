import json
from . import app, client, cache, create_token_int, create_token_non, create_token_for_book, create_token_for_book_2, reset_database

class TestAuth():
  reset_database()

  def test_unauthorized(self, client):
    data = {
            'user_name' : 'alzimnaea',
            'password' : 'password'
        }
        
    res = client.get('/login', query_string=data,content_type='application/json')
    assert res.status_code == 401
  
  def test_post(self,client):
    token = create_token_for_book()
    res = client.post('/login', headers={'Authorization' : "Bearer "+token}, content_type='application/json')
    assert res.status_code == 200

  def test_refresh(self,client):
    token = create_token_for_book()
    res = client.post('/login/refresh', headers={'Authorization' : "Bearer "+token}, content_type='application/json')
    assert res.status_code == 200
  
  def test_option(self,client):
    res = client.options('/login',content_type='application/json')

    assert res.status_code == 200
