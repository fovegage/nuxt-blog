"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from shop.settings import MEDIA_ROOT
from goods.tests import GoodView
from django.conf.urls import url, include
from goods.views import GoodListViewSet, GoodCategoryViewSet, GoodCategoryBrandViewSet, CategoryBrandViewSet
from users.views import SMSViewSet, UserRegisterViewSet, UserAddressViewSet, WeiboLogin, trigger_error
from trades.views import ShoppingCartViewSet, PayInfoViewSet, AliPayViewSet
from operation.views import UserFavViewSet, UserMessageViewSet
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls
from django.views.generic import TemplateView

routers = DefaultRouter()
routers.register(r'goods', GoodListViewSet)
routers.register(r'categorys', GoodCategoryViewSet)
routers.register(r'code', SMSViewSet, base_name='codes')
routers.register(r'users', UserRegisterViewSet, base_name='register')
routers.register(r'userfavs', UserFavViewSet, base_name='user_fav')
routers.register(r'messages', UserMessageViewSet, base_name='messages')
routers.register(r'address', UserAddressViewSet, base_name='address')
routers.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')
routers.register(r'orders', PayInfoViewSet, base_name='orders')
routers.register(r'banners', GoodCategoryBrandViewSet, base_name='banners')
routers.register(r'indexgoods', CategoryBrandViewSet, base_name='indexgoods')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(routers.urls)),
    # path('return/$', PayViewSet.as_view()),
    url(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt
    url(r'^login/$', obtain_jwt_token),
    # 文档
    url(r'docs/', include_docs_urls(title='嘉美伯爵')),
    # path('docs/', include_docs_urls(title='嘉美伯爵'))
    # path('swagger-ui/', TemplateView.as_view(
    #     template_name='swagger-ui.html',
    #     extra_context={'schema_url': 'openapi-schema'}
    # ), name='swagger-ui'),
    url(r'^alipay/return/', AliPayViewSet.as_view(), name="alipay"),
    url(r'weibo/', WeiboLogin.as_view(), name='weibologin'),
    # path('sentry-debug/', trigger_error),
]
