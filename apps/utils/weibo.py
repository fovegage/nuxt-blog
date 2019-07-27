# -*- coding: utf-8 -*-
from shop.settings import redirect_uri

# https://api.weibo.com/oauth2/authorize?client_id=123050457758183&redirect_uri=http://www.example.com/response&response_type=code

class Weibo:
    def __init__(self, client_id, client_secret=None, code=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code

    def get_weibo_login_code(self):
        weibo_oauth2_url = 'https://api.weibo.com/oauth2/authorize?client_id={}'.format(self.client_id)
        redirect_url = 'http://139.199.123.96:8000/weibo/'
        send_url = weibo_oauth2_url + '&redirect_uri={}'.format(redirect_url)
        return send_url

    def get_access_token(self):
        import requests
        api = 'https://api.weibo.com/oauth2/access_token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': self.code,
            'redirect_uri': redirect_uri
        }
        response = requests.post(api, data=data)
        return response.json()


if __name__ == '__main__':
    w = Weibo('569009949')
    print(w.get_weibo_login_code())
