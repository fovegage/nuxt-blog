# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import ShoppingCart, OrderInfo, PayInfo
from goods.models import Good
from goods.serializers import GoodSerializer
from utils import gen_order_no
from utils.alipay import AliPay
from shop.settings import private_key, alipay_public_key

class OrderInfoSerializer(serializers.ModelSerializer):
    goods = GoodSerializer(many=False)

    class Meta:
        model = OrderInfo
        fields = '__all__'


class PayDetailSerializer(serializers.ModelSerializer):
    goods = OrderInfoSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016101000652414",
            app_notify_url="http://139.199.123.96:8000/alipay/return/",
            app_private_key_path=private_key,
            alipay_public_key_path=alipay_public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://139.199.123.96:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.money,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    # 序列化时生成订单号
    def validate(self, attrs):
        attrs['order_sn'] = gen_order_no(self.context['request'])
        return attrs

    class Meta:
        model = PayInfo
        fields = '__all__'


class PayInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_sn = serializers.CharField(read_only=True)

    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, obj):
        alipay = AliPay(
            appid="2016101000652414",
            app_notify_url="http://139.199.123.96:8000/alipay/return/",
            app_private_key_path=private_key,
            alipay_public_key_path=alipay_public_key,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://139.199.123.96:8000/alipay/return/"
        )

        url = alipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.money,
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return re_url

    # 序列化时生成订单号
    def validate(self, attrs):
        attrs['order_sn'] = gen_order_no(self.context['request'])
        return attrs

    class Meta:
        model = PayInfo
        fields = '__all__'


class ShoppingDetailSerializer(serializers.ModelSerializer):
    goods = GoodSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ['goods', 'nums']


class ShoppingCartSerializer(serializers.Serializer):
    # 使用 Serializer 需要自定义 不能 Meta
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goods = serializers.PrimaryKeyRelatedField(queryset=Good.objects.all(), required=True)
    nums = serializers.IntegerField(min_value=1, error_messages={'min_value': '数量必须大于1'}, required=True)

    # post 进行修改操作
    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']
        is_exist = ShoppingCart.objects.filter(user=user, goods=goods)
        if is_exist:
            cart_object = is_exist[0]
            cart_object.nums += nums
            cart_object.save()
        else:
            cart_object = ShoppingCart.objects.create(**validated_data)

        return cart_object

    # put 进行更新操作
    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance
