from rest_framework.views import APIView
from django.shortcuts import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingDetailSerializer, PayInfoSerializer, PayDetailSerializer
from .models import ShoppingCart, PayInfo, OrderInfo


class PayInfoViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    订单的创建、取消、删除
    """
    # serializer_class = PayInfoSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PayDetailSerializer
        return PayInfoSerializer

    # 进行遍历保存
    def perform_create(self, serializer):
        order = serializer.save()
        shop_cart = ShoppingCart.objects.filter(user=self.request.user)

        if shop_cart:
            for item in shop_cart:
                child_order = OrderInfo()
                child_order.goods = item.goods
                child_order.nums = item.nums
                child_order.pay = order
                child_order.save()
                # 减少库存
                good = item.goods
                good.good_num -= item.nums
                good.save()
                shop_cart.delete()
            return order

    def perform_destroy(self, instance):
        # 取消订单增加库存
        is_exist = OrderInfo.objects.filter(pay__order_sn=instance.order_sn)
        if is_exist:
            for item in is_exist:
                item.goods.good_num += item.nums
                item.goods.save()
        instance.delete()

    def get_queryset(self):
        return PayInfo.objects.filter(user=self.request.user)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    # serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'  # 根据 good.id 查询详情

    # serializer_class 失效
    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingDetailSerializer
        else:
            return ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


# class AliPayViewSet(APIView):
#     def get(self, request):
#         from utils import handle_django_query_dict
#         # print(type(request.GET), request.GET)
#         print(handle_django_query_dict(request.GET))
#         get_pay_dcit = {}
#         return_data = request.GET.items()
#         for key, item in return_data:
#             get_pay_dcit[key] = item
#         sign = get_pay_dcit.pop('sign', None)
#         # print(get_pay_dcit)
#
#     def post(self, request):
#         pass
from rest_framework.views import APIView
from utils.alipay import AliPay
from shop.settings import private_key, alipay_public_key
from rest_framework.response import Response
from datetime import datetime
from django.shortcuts import redirect


class AliPayViewSet(APIView):
    def get(self, request):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016101000652414",
            app_notify_url="http://139.199.123.96:8000/alipay/return/",
            app_private_key_path=private_key,
            alipay_public_key_path=alipay_public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://139.199.123.96:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            return HttpResponse('支付成功')
            response = redirect("index")
            response.set_cookie("nextPath", "pay", max_age=3)
            return response
        else:
            response = redirect("index")
            return response

    def post(self, request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid="2016101000652414",
            app_notify_url="http://139.199.123.96:8000/alipay/return/",
            app_private_key_path=private_key,
            alipay_public_key_path=alipay_public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://139.199.123.96:8000/alipay/return/"
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = PayInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.nums
                    goods.save()

                existed_order.status = trade_status
                existed_order.pay_sn = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            return Response("success")
