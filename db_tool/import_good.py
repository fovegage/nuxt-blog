# -*- coding: utf-8 -*-
import os
import sys

pwd = os.path.dirname(os.path.dirname(__file__))

# 进入django设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

import django

django.setup()

from goods.models import Good, GoodCategory, GoodCarouselImage
from db_tool.data.product_data import row_data

for goods_detail in row_data:
    goods = Good()
    goods.name = goods_detail["name"]
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.sold_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
    goods.good_desc = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.good_detail = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    goods.cover = goods_detail["images"][0] if goods_detail["images"] else ""

    category_name = goods_detail["categorys"][-1]
    category = GoodCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodCarouselImage()
        goods_image_instance.image = goods_image
        goods_image_instance.good = goods
        goods_image_instance.save()
