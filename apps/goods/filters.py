# -*- coding: utf-8 -*-
import django_filters
from .models import Good


class GoodsFilter(django_filters.rest_framework.FilterSet):
    price_min = django_filters.NumberFilter(field_name='sold_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='sold_price', lookup_expr='lte')

    class Meta:
        model = Good
        fields = ['price_min', 'price_max', 'is_hot', 'is_new']
