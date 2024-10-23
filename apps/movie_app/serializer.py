from rest_framework import serializers
from .models import MovieGenre, Movie


class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGenre
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'slug')
        extra_kwargs = {'description': {'required': True}}


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'slug')
