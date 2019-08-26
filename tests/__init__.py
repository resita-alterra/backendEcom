import pytest, json, logging
from flask import Flask, request

from blueprints import app
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


def create_token_non():
    token = cache.get('test-token-non')
    if token is None:
        data = {
            'user_name' : 'userdummy',
            'password' : 'password'
        }
        # do request
        req = call_client(request)
        res = req.get('/login', query_string=data,content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json )
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token-non',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token

def create_token_for_book():
    token = cache.get('test-token-for-book')
    if token is None:
        data = {
            'user_name' : 'alzimnae',
            'password' : 'password'
        }
        # do request
        req = call_client(request)
        res = req.get('/login', query_string=data,content_type='application/json')

        # store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json )
        # assert if the result is as expected
        assert res.status_code == 200

        # save token into cache
        cache.set('test_token-for-book',res_json['token'], timeout=60)

        return res_json['token']
    else:
        return token