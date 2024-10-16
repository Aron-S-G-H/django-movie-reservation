from rest_framework import serializers
from .models import MovieGenre


class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGenre
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'slug')
        extra_kwargs = {'description': {'required': True}}
