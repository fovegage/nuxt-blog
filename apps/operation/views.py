from rest_framework import viewsets, mixins
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserFavSerializer, UserCollectSerializer, UserMessageSerializer
from .models import UserFav, UserMessage
from utils.permissions import IsOwnerOrReadOnly


class UserMessageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = UserMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 权限验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 不在setting配置,以免全局生效

    def get_queryset(self):
        return UserMessage.objects.filter(user=self.request.user)


# list retrieve create destroy
class UserFavViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 权限验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)  # 不在setting配置,以免全局生效
    lookup_field = 'good_id'

    def get_queryset(self):
        # 重写queryset 针对单个用户
        return UserFav.objects.filter(user=self.request.user)

    # 与django信号量选择一个
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     good = instance.good
    #     good.fav_num += 1
    #     good.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserCollectSerializer
        else:
            return UserFavSerializer
