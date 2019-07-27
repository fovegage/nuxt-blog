# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Good, GoodCategory, GoodCarouselImage, GoodCategoryBrand, CarouselGood, IndexAD


class GoodCarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodCarouselImage
        fields = ('image',)


class GoodCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodCategory
        fields = '__all__'


class GoodCategorySerializer2(serializers.ModelSerializer):
    sub_cat = GoodCategorySerializer3(many=True)

    class Meta:
        model = GoodCategory
        fields = '__all__'


class GoodCategorySerializer(serializers.ModelSerializer):
    sub_cat = GoodCategorySerializer2(many=True)

    class Meta:
        model = GoodCategory
        fields = '__all__'


class GoodSerializer(serializers.ModelSerializer):
    # 继承 Serializer 需要手动书写
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=100)
    category = GoodCategorySerializer()
    images = GoodCarouselImageSerializer(many=True)

    class Meta:
        model = Good
        fields = "__all__"  # 可以用 [] 进行指定

    # 取来自view验证的数据，创建对象
    def create(self, validated_data):
        return Good.objects.create(**validated_data)


class CarouselGoodSerializer(serializers.ModelSerializer):
    """
    轮播商品序列化
    """

    class Meta:
        model = CarouselGood
        fields = "__all__"  # 可以用 [] 进行指定


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodCategoryBrand
        fields = "__all__"  # 可以用 [] 进行指定


class CategoryBrandAdSerializer(serializers.ModelSerializer):
    """
    商品下属商标和广告序列化
    """
    sub_cat = GoodCategorySerializer2(many=True)
    banner = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    ad_goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        from django.db.models import Q
        all_goods = Good.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        return GoodSerializer(all_goods, many=True, context={'request': self.context['request']}).data

    def get_ad_goods(self, obj):
        # 反查
        ad_goods = {}
        is_exist = IndexAD.objects.filter(category_id=obj.id)
        if is_exist:
            goods = is_exist[0]
            return GoodSerializer(goods.good, many=False, context={'request': self.context['request']}).data

    class Meta:
        model = GoodCategory
        fields = "__all__"  # 可以用 [] 进行指定
