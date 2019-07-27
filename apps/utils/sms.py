# -*- coding: utf-8 -*-
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from shop.settings import appid, appkey
import json


class Tencent_SMS:
    def __init__(self, mobile, code):
        self.mobile = mobile
        self.params = [code, '3']

    def send_code(self):
        ssender = SmsSingleSender(appid, appkey)
        try:
            result = ssender.send_with_param(86, self.mobile,
                                             378910, self.params, sign='', extend="", ext="")

            return result
        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    sms = Tencent_SMS('18553713028', '12121')
    sms.send_code()
