# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
import datetime
import re
from .models import VerifyCode, UserInfo, UserAddress

user = get_user_model()


class SMSSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    # 验证手机号
    def validate_mobile(self, mobile):
        # 验证是否存在
        if user.objects.filter(mobile=mobile):
            raise serializers.ValidationError('手机号码已经存在')
        # 验证是否合法
        if not re.match(r"^1[35678]\d{9}$", mobile):
            raise serializers.ValidationError('手机号码格式不正确')
        # 验证是否间隔一分钟
        is_one_minutes = datetime.datetime.now() - datetime.timedelta(minutes=1)
        if VerifyCode.objects.filter(add_time__gt=is_one_minutes, mobile=mobile):
            raise serializers.ValidationError('距上次发送不足1分钟')

        return mobile


class UserRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=6, help_text='验证码',
                                 label='验证码')
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True
    )

    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=user.objects.all(), message="用户已经存在")])

    class Meta:
        model = UserInfo
        fields = ['username', 'code', 'mobile', 'password']

    # 验证验证码
    def validate_code(self, code):
        last_record = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if last_record:
            if last_record[0].code != code:
                raise serializers.ValidationError('验证码无效')
            # 验证三分钟内有效
            is_three_minutes = datetime.datetime.now() - datetime.timedelta(minutes=3)
            last_time = last_record[0].add_time.replace(tzinfo=None)
            if last_record[0].add_time.replace(tzinfo=None) > is_three_minutes:
                raise serializers.ValidationError('验证码已经失效,请重新获取')

        else:
            raise serializers.ValidationError('验证码错误')

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['nickname', 'birthday', 'gender', 'email', 'mobile']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'

    add_time = serializers.DateTimeField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


