# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav, UserMessage
from goods.serializers import GoodSerializer


class UserMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')

    # 只返回 不提交
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%S')


class UserCollectSerializer(serializers.ModelSerializer):
    good = GoodSerializer()

    class Meta:
        model = UserFav
        fields = ['good', 'id']


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=['good', 'user'],
                message='已经搜藏'
            )
        ]
        fields = ['user', 'good', 'id']
