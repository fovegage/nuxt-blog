# -*- coding: utf-8 -*-
from string import digits
from Crypto.Signature import PKCS1_v1_5
# from alipay.aop.api.util.SignatureUtils import sign_with_rsa2, fill_private_key_marker, verify_with_rsa, \
#     fill_public_key_marker
from Crypto.Hash import SHA256
from base64 import encodebytes, decodebytes
import random
import time
import rsa


def gen_random_str():
    return ''.join([random.choice(digits) for x in range(6)])


def gen_order_no(request):
    return '{current_time_str}{user_id}{random_str}'.format(current_time_str=time.strftime('%Y%m%d%H%M%S'),
                                                            user_id=request.user.id,
                                                            random_str=gen_random_str())


a = {'charset': 'utf-8', 'out_trade_no': '91922212229232131', 'method': 'alipay.trade.page.pay.return',
     'total_amount': '10.00',
     'sign': 'G3aHQ0QU9ika/YrCPVCb9MWP4oShI5Q8+Zm6M0KvF5Dfom+OkczPrrIQSTMfb9Ml/nU6WkasQjgjw9UyPXPWSI/5ka4XkaxPTdz3n/eG4oTuQ7P/zmfuVHIP2mppha4H6VvoytovJXgGifuCvyVRHRB7kmOj62boj7wWeD3hxxNt/US+FYB457tX8GZdA4IQNtzYVm70wLjXhf4GawfDIqcj+R3eNbgaPSjutmSpPrOiM8Tm3Jh0vmd6urHXMvf3uFWJ0+BzKngFvjaa48gW0cBygLYHXso8qinUXkGE3blckiP6MP1x7CUwjqIx+YZVmS5ID2zRxGcDLheG5eUbrA==',
     'trade_no': '2019072522001497951000027682', 'auth_app_id': '2016101000652414', 'version': '1.0',
     'app_id': '2016101000652414', 'sign_type': 'RSA2', 'seller_id': '2088102178920860',
     'timestamp': '2019-07-25 14:52:07'}


def data_sign(data):
    key = 'MIIEpAIBAAKCAQEAz/a0a9vclQSju1lnpI0xecl4StHW+FXnVAwmBKhbYb+Q42jIaXwIu6rxjbj8ZqxTQ5HWM2gKk090wAfeLSRqMkJJ47vHW3W8bN3aTyU+tsH0ZZRCVRqnjfDB8VYj/tiAvP2ZhwaGpAMvfm7fdQ8JcCeiVCqLmsO5Il6LbincNtoxeXWrDe8F7VAOtNoScxN1pD8PQBrkjALInZRID56lCkPQ39ZDrA1IvoWbBsdyfDJ/U1xWVLuyjp7L2cBgKL9yfxiOmI3ZjX5Rk57pUD0j2936R3OuEcPl5P+vALCkRD6kVZDeV8qNXK83eXouj0co6KuiBGV3KyMYUCBoyy/JawIDAQABAoIBAEjixR8cQnXz11KdJgb0+UcexksqujX1HYtGaritLMHYevZIzhyyPPlREzHBiKyPbus6nKENsM8qRNfcqhCWN6X/t5faQyeZ3v0k0BN3EUDKP1aunITpP5ourDpiH2F9DbmvA/Tf46Zt+2JLh4OmTn+BVJI9Cwql2CfkjOeCQkzykC9NjIZzsQMCZ1hg3yXDsFLsSRWPGzVxDJ6VnyjWLuWsm1l/MrRYLWro7ZzdW2XmD+0KdDMSM6YTc4gaYnuoBNynE2e3KkiOJHiAlp++ZEbQrVwSIcnygH7CwQSNqAQ/kcJaOL6i+9lIxrsLdKhhs4UBj4Te+TgDkKhIN64zr1ECgYEA6WvkbLzXuq51cojIknAt1IZglMZFK9ghzxmubsZoCLhHftcVkhFB8yGjWNbDhKwyx4r6mVzEgJ5C7nquJxXKDB8UB6UTZIjLLS5+lE7eu1QcyXaRnHiFYfuswQSp7CeTSQyHlcMFV3ZQqv1m3fYBkXfoUvQKUwqxzbe3eYguU3MCgYEA5BRp5AcEEBa5xYYzAjG+QGDhQOlPQQ+rf4KOxa0PyGbx0jeJBRyNDmdNwwUsLBoCwF0UisN9ArOMUYMSasKSbCbubNE7r5dB/kJc6tdWzpCMhsXD/RzEvC6RYU2XoyBL1wXlcEtCCMTZFO3pvt+pnKvEHdoVUzGyuAjHoHhG5CkCgYEAg5mttlSduAVl+AYANveCD0EXsKk8FGUNYqrS+mdn/gqPXIa9BZYvPXlok8y5fNJs6q2DbfWsX+taRwPpreWN/VmEPG8oSNUK39VHzivNTYY1mKv9ml8krEJteoE7oAYL9vJWeuvx1gbBojWtylRJPA+Db0lhjMIJzrbWfXF21NsCgYEAjw8q2Cd6aekHPxkM15yB2/mocEGnP4TnqkQm72C83JONrLC+1iDxbQ5o3SFacpMiFKyNnPg/ajlakyomnCZNF19X/5NB38J9V1Ei3P6S6WALdOGJLDMmR27iK2ky6tPwHgAJyOS7l6p5C0Krcdjyl1251oubAqLSmdKP/FxVAvkCgYBgDO/wWYws2HIS8M+PTJPm8sIf8ZxHOondGMbz9wildAkAQ910cL0MAw9L2p2hsnsoGOVFQCBBUhxaNLgXXkL6TBYZuXeBOFsn3CJs2gwrTf4ew96/n0VvTmnZmSQnYlYihgJXGvKJE+MDMZ2MWA0DitKz/Mi6eNY0VmLvAJqBAg=='
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA256.new(data_join(data).encode('utf-8')))
    # base64 编码，转换为unicode表示并移除回车
    sign = encodebytes(signature).decode("utf8").replace("\n", "")
    return sign


def data_join(data):
    return '&'.join('{key}={item}'.format(key=key, item=item) for key, item in dict_sort(data).items())


def dict_sort(data):
    dict_sorted = {}
    for key in sorted(data):
        dict_sorted[key] = data[key]
    dict_sorted.pop('sign', None)
    return dict_sorted


def handle_django_query_dict(data):
    return dict([(key, item) for key, item in data.items()])


key = 'MIIEpAIBAAKCAQEAz/a0a9vclQSju1lnpI0xecl4StHW+FXnVAwmBKhbYb+Q42jIaXwIu6rxjbj8ZqxTQ5HWM2gKk090wAfeLSRqMkJJ47vHW3W8bN3aTyU+tsH0ZZRCVRqnjfDB8VYj/tiAvP2ZhwaGpAMvfm7fdQ8JcCeiVCqLmsO5Il6LbincNtoxeXWrDe8F7VAOtNoScxN1pD8PQBrkjALInZRID56lCkPQ39ZDrA1IvoWbBsdyfDJ/U1xWVLuyjp7L2cBgKL9yfxiOmI3ZjX5Rk57pUD0j2936R3OuEcPl5P+vALCkRD6kVZDeV8qNXK83eXouj0co6KuiBGV3KyMYUCBoyy/JawIDAQABAoIBAEjixR8cQnXz11KdJgb0+UcexksqujX1HYtGaritLMHYevZIzhyyPPlREzHBiKyPbus6nKENsM8qRNfcqhCWN6X/t5faQyeZ3v0k0BN3EUDKP1aunITpP5ourDpiH2F9DbmvA/Tf46Zt+2JLh4OmTn+BVJI9Cwql2CfkjOeCQkzykC9NjIZzsQMCZ1hg3yXDsFLsSRWPGzVxDJ6VnyjWLuWsm1l/MrRYLWro7ZzdW2XmD+0KdDMSM6YTc4gaYnuoBNynE2e3KkiOJHiAlp++ZEbQrVwSIcnygH7CwQSNqAQ/kcJaOL6i+9lIxrsLdKhhs4UBj4Te+TgDkKhIN64zr1ECgYEA6WvkbLzXuq51cojIknAt1IZglMZFK9ghzxmubsZoCLhHftcVkhFB8yGjWNbDhKwyx4r6mVzEgJ5C7nquJxXKDB8UB6UTZIjLLS5+lE7eu1QcyXaRnHiFYfuswQSp7CeTSQyHlcMFV3ZQqv1m3fYBkXfoUvQKUwqxzbe3eYguU3MCgYEA5BRp5AcEEBa5xYYzAjG+QGDhQOlPQQ+rf4KOxa0PyGbx0jeJBRyNDmdNwwUsLBoCwF0UisN9ArOMUYMSasKSbCbubNE7r5dB/kJc6tdWzpCMhsXD/RzEvC6RYU2XoyBL1wXlcEtCCMTZFO3pvt+pnKvEHdoVUzGyuAjHoHhG5CkCgYEAg5mttlSduAVl+AYANveCD0EXsKk8FGUNYqrS+mdn/gqPXIa9BZYvPXlok8y5fNJs6q2DbfWsX+taRwPpreWN/VmEPG8oSNUK39VHzivNTYY1mKv9ml8krEJteoE7oAYL9vJWeuvx1gbBojWtylRJPA+Db0lhjMIJzrbWfXF21NsCgYEAjw8q2Cd6aekHPxkM15yB2/mocEGnP4TnqkQm72C83JONrLC+1iDxbQ5o3SFacpMiFKyNnPg/ajlakyomnCZNF19X/5NB38J9V1Ei3P6S6WALdOGJLDMmR27iK2ky6tPwHgAJyOS7l6p5C0Krcdjyl1251oubAqLSmdKP/FxVAvkCgYBgDO/wWYws2HIS8M+PTJPm8sIf8ZxHOondGMbz9wildAkAQ910cL0MAw9L2p2hsnsoGOVFQCBBUhxaNLgXXkL6TBYZuXeBOFsn3CJs2gwrTf4ew96/n0VvTmnZmSQnYlYihgJXGvKJE+MDMZ2MWA0DitKz/Mi6eNY0VmLvAJqBAg=='
pub = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz/a0a9vclQSju1lnpI0xecl4StHW+FXnVAwmBKhbYb+Q42jIaXwIu6rxjbj8ZqxTQ5HWM2gKk090wAfeLSRqMkJJ47vHW3W8bN3aTyU+tsH0ZZRCVRqnjfDB8VYj/tiAvP2ZhwaGpAMvfm7fdQ8JcCeiVCqLmsO5Il6LbincNtoxeXWrDe8F7VAOtNoScxN1pD8PQBrkjALInZRID56lCkPQ39ZDrA1IvoWbBsdyfDJ/U1xWVLuyjp7L2cBgKL9yfxiOmI3ZjX5Rk57pUD0j2936R3OuEcPl5P+vALCkRD6kVZDeV8qNXK83eXouj0co6KuiBGV3KyMYUCBoyy/JawIDAQAB'
print(data_join(a))


# private = fill_private_key_marker(key)
# public = fill_public_key_marker(pub)
# message = sign_with_rsa2(key, data_join(a), 'utf-8')
# print(message)
# print(verify_with_rsa(pub, data_join(a), a['sign']))
import base64


# def verify_with_rsa(public_key, message, sign):
#     public_key = fill_public_key_marker(public_key)
#     sign = base64.b64decode(sign)
#     return bool(rsa.verify(message, sign, rsa.PublicKey.load_pkcs1_openssl_pem(public_key)))
