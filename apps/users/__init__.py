def get_access_token():
    import requests
    api = 'https://api.weibo.com/oauth2/access_token'
    data = {
        'client_id': '569009949',
        'client_secret': '346e934331ad3d0543e73ca567ec28c1',
        'grant_type': 'authorization_code',
        'code': '06f3242383f849c051f95f6f3a5b3650',
        'redirect_uri': 'http://139.199.123.96:8000/weibo/'
    }
    response = requests.post(api, data=data)
    print(response.json())

get_access_token()
