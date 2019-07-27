from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.db.models import Q
from .models import UserInfo
from utils.sms import Tencent_SMS
from utils import gen_random_str
from utils.permissions import IsOwnerOrReadOnly
from .serializers import SMSSerializer, UserRegisterSerializer, UserDetailSerializer, UserAddressSerializer
from .models import VerifyCode, UserAddress
from utils.weibo import Weibo
from shop.settings import client_id, client_secret, redirect_uri


User = get_user_model()


class WeiboLogin(APIView):
    def get(self, request):
        code = request.GET.get('code')
        weibo = Weibo(client_id, client_secret, code)
        print(weibo.get_access_token())



class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SMSViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SMSSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        code = gen_random_str()
        sms_response = Tencent_SMS(mobile, code).send_code()
        if sms_response['errmsg'] != 'OK':
            return Response({'mobile': sms_response['errmsg']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(mobile=mobile, code=code)
            code_record.save()
            return Response({'mobile': mobile}, status=status.HTTP_201_CREATED)


class UserRegisterViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    # 添加权限
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 鉴权
    # permission_classes = (IsAuthenticated,)

    # 动态鉴权
    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        elif self.action == 'create':
            return []

        return []

    def get_object(self):
        # 只返回单个用户
        return self.request.user

    # 动态序列化
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegisterSerializer

        return UserDetailSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

# sentry测试
def trigger_error(request):
    division_by_zero = 1 / 0