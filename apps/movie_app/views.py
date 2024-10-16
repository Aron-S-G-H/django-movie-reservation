from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .serializer import MovieGenreSerializer
from.models import MovieGenre


@extend_schema(request=MovieGenreSerializer, responses=MovieGenreSerializer, tags=['Movie Genre'])
class MovieGenreViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = MovieGenre.objects.all()
        serializer = MovieGenreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(MovieGenre, pk=pk)
        serializer = MovieGenreSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = MovieGenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'response': 'Created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        instance = get_object_or_404(MovieGenre, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = MovieGenreSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response('Updated successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = get_object_or_404(MovieGenre, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response('Deleted successfully', status=status.HTTP_200_OK)
