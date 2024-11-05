from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializer import UserSerializer, UserLoginSerializer, UserRegisterSerializer
from .permissions import UserHasPermissionOrReadOnly
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenRefreshView
from .utils import get_tokens
from . import decorators


@extend_schema(tags=['Authentication and Authorization'])
class UserAuthenticationViewSet(ViewSet):
    @decorators.user_login_decorator
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

    @decorators.user_register_decorator
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

    @decorators.token_refresh_decorator
    def token_refresh(self, request):
        return TokenRefreshView.as_view()(request._request)


@extend_schema(tags=['User account'])
class UserViewSet(ViewSet):
    permission_classes = [IsAuthenticated, UserHasPermissionOrReadOnly]

    @decorators.users_list_decorator
    def list(self, request):
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.user_retrieve_decorator
    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.user_update_decorator
    def update(self, request, pk=None):
        instance = get_object_or_404(CustomUser, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = UserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response({"response": "Updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.user_delete_decorator
    def destroy(self, request, pk):
        instance = get_object_or_404(CustomUser, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({"response": "Deleted successfully"}, status=status.HTTP_200_OK)
