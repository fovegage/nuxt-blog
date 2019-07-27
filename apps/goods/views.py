from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .models import Good, GoodCategory, GoodCategoryBrand, CarouselGood
from .serializers import GoodSerializer, GoodCategorySerializer, CarouselGoodSerializer, CategoryBrandAdSerializer
from .filters import GoodsFilter


class CategoryBrandViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategoryBrandAdSerializer
    queryset = GoodCategory.objects.filter(is_banner=True)


class GoodCategoryBrandViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CarouselGoodSerializer
    queryset = CarouselGood.objects.all()


class GoodPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class GoodListViewSet(CacheResponseMixin, ListAPIView, RetrieveModelMixin, viewsets.GenericViewSet):
    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    pagination_class = GoodPagination
    # authentication_classes = [JSONWebTokenAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['name', 'sold_price'] # 精确查找
    filter_class = GoodsFilter
    search_fields = ['name']
    ordering_fields = ['sold_num', 'sold_price']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # 继承 ListAPIView viewsets.GenericViewSet
    # 需要在 urls.py 配置 注意两种路由的注册方式
    # good_list = GoodList.as_view({
    #     'get': 'list',
    #
    # })
    # path('good_list/', good_list),

    # 继承 ListAPIView
    # queryset = Good.objects.all()
    # serializer_class = GoodSerializer

    # 继承 ListModelMixin, GenericAPIView
    # queryset = Good.objects.all()
    # serializer_class = GoodSerializer
    #
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

    # 继承 APIView
    # # 查询
    # def get(self, request, format=None):
    #     goods = Good.objects.all()
    #     goods_serializers = GoodSerializer(goods, many=True)
    #     return Response(goods_serializers.data)
    #
    # # 添加
    # def post(self, request, format=None):
    #     good_serializer = GoodSerializer(data=request.data)
    #     if good_serializer.is_valid():
    #         good_serializer.save()
    #         return Response(good_serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(good_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodCategoryViewSet(ListAPIView, RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodCategory.objects.filter(category_type=1)
    serializer_class = GoodCategorySerializer
