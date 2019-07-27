from datetime import datetime
from django.db import models
from users.models import UserInfo
from goods.models import Good


class UserFav(models.Model):
    user = models.ForeignKey(to=UserInfo, verbose_name='用户', on_delete=models.CASCADE)
    good = models.ForeignKey(to=Good, verbose_name='商品', on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户搜藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.nickname


class UserMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(UserInfo, verbose_name="用户", on_delete=models.CASCADE)
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name="留言类型",
                                       help_text="留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = models.CharField(max_length=100, default="", verbose_name="主题")
    message = models.TextField(default="", verbose_name="留言内容", help_text="留言内容")
    file = models.FileField(upload_to="messages/images/", verbose_name="上传的文件", help_text="上传的文件")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject
