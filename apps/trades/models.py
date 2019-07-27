from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Good

User = get_user_model()


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(to=User, verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey(to=Good, verbose_name='商品', on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name='购买数量')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%d)'.format(self.goods.name, self.nums)


class PayInfo(models.Model):
    """
    支付表
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "成功"),
        ("TRADE_CLOSED", "超时关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("paying", "待支付"),
    )

    PAY_TYPE = (
        ('alipay', '支付宝'),
        ('wechat', '微信')
    )
    user = models.ForeignKey(to=User, verbose_name='用户', on_delete=models.CASCADE)
    order_sn = models.CharField(verbose_name='订单编号', default='', null=True, blank=True, unique=True, max_length=50)
    pay_sn = models.CharField(verbose_name='支付编号', default='', null=True, blank=True, max_length=50)
    status = models.CharField(verbose_name='订单状态', default='paying', choices=ORDER_STATUS, max_length=30)
    money = models.FloatField(verbose_name='订单金额')
    message = models.CharField(verbose_name='订单留言', max_length=200)
    pay_time = models.DateTimeField(verbose_name='支付时间', default=datetime.now)

    # 用户信息 注意这里不要用外键 外键把值传给它
    address = models.CharField(max_length=100, default="", verbose_name="收货地址")
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    singer_mobile = models.CharField(max_length=11, default='', verbose_name="联系电话")

    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '支付信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%d)'.format(self.user, self.money)


class OrderInfo(models.Model):
    """
    商品所属订单表,后期考虑子订单, 详情
    """
    pay = models.ForeignKey(to=PayInfo, verbose_name='支付信息', on_delete=models.CASCADE, related_name='goods')
    goods = models.ForeignKey(to=Good, verbose_name='商品', on_delete=models.CASCADE)
    nums = models.IntegerField(default=0, verbose_name='购买数量')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s(%d)'.format(self.goods.name, self.nums)