from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializer import UserSerializer, UserLoginSerializer, UserRegisterSerializer
from .permissions import UserHasPermissionOrReadOnly
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .utils import get_tokens
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


@extend_schema(tags=['Authentication and Authorization'])
class UserAuthenticationViewSet(ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(request=UserLoginSerializer)
    @action(methods=['POST'], url_path='login', detail=False, url_name='login')
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens(user=user)
            return Response({
                **tokens,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=UserRegisterSerializer)
    @action(methods=['POST'], url_path='register', detail=False, url_name='register')
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens(user=user)
            return Response({
                **tokens,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=TokenRefreshSerializer)
    @action(methods=['POST'], url_path='token/refresh', detail=False, url_name='refresh_token')
    def token_refresh(self, request):
        return TokenRefreshView.as_view()(request._request)


@extend_schema(request=UserSerializer, responses=UserSerializer, tags=['User account'])
class UserViewSet(ViewSet):
    permission_classes = [UserHasPermissionOrReadOnly]

    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        instance = get_object_or_404(CustomUser, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = UserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response('Updated successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = get_object_or_404(CustomUser, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response('Deleted successfully', status=status.HTTP_200_OK)