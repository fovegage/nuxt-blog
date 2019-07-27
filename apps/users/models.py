from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户表
    """
    # null blank default
    nickname = models.CharField(verbose_name='昵称', default='', max_length=20)
    birthday = models.DateField(verbose_name='生日', blank=True, null=True, default=None)
    mobile = models.CharField(null=True, blank=True, default='', verbose_name='手机号', max_length=11)
    gender = models.CharField(verbose_name='性别', choices=(('male', '男'), ('female', '女')), default='', max_length=6)
    email = models.CharField(verbose_name='邮箱', default='', max_length=50)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField(verbose_name='验证码', max_length=6)
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class UserAddress(models.Model):
    """
    收货地址
    """
    user = models.ForeignKey(to=UserInfo, verbose_name='用户', on_delete=models.CASCADE)
    province = models.CharField(max_length=50, default="", verbose_name="省份")
    city = models.CharField(max_length=50, default="", verbose_name="城市")
    district = models.CharField(max_length=50, default="", verbose_name="区域")
    address = models.CharField(max_length=100, default="", verbose_name="详细地址")
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, default="", verbose_name="电话")
    stamp = models.CharField(default='', null=True, blank=True, verbose_name='邮编', max_length=6)
    is_select = models.BooleanField(default=False, verbose_name='是否默认')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

class ThirdPartyLogin(models.Model):
    uid = models.CharField(verbose_name='uid', max_length=100)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

