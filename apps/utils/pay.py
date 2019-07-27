# -*- coding: utf-8 -*-
# 统一收单下单并支付页面接口
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient


# from shop.settings import private_key, alipay_public_key


class AliPay:
    def __init__(self, private_key, alipay_public_key):
        with open(private_key) as f:
            self.private_key = f.read()

        with open(alipay_public_key) as f:
            self.app_private_key = f.read()

        alipay_client_config = AlipayClientConfig(sandbox_debug=True)
        alipay_client_config.app_id = '2016101000652414'
        alipay_client_config.app_private_key = self.private_key
        alipay_client_config.alipay_public_key = self.app_private_key
        self.client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

    def trade_page_pay(self):
        page_pay = AlipayTradePagePayModel()
        page_pay.out_trade_no = 91922212229232131
        page_pay.product_code = 'FAST_INSTANT_TRADE_PAY'
        page_pay.total_amount = 10
        page_pay.subject = '测试'
        request = AlipayTradePagePayRequest(biz_model=page_pay)
        request.return_url = 'http://139.199.123.96:8000/alipay/return/'
        request.notify_url = 'http://139.199.123.96:8000/alipay/return/'
        response = self.client.page_execute(request, http_method="GET")
        print("alipay.trade.page.pay response:" + response)
        return response


if __name__ == '__main__':
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    private_key = os.path.join(BASE_DIR, 'utils/key/private_2048.txt')
    alipay_public_key = os.path.join(BASE_DIR, 'utils/key/key.txt')
    pay = AliPay(private_key, alipay_public_key)
    pay.trade_page_pay()