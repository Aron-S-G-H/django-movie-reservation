from rest_framework import serializers
from .models import MovieGenre, Movie
from drf_spectacular.utils import extend_schema_field


class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGenre
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'slug')
        extra_kwargs = {'description': {'required': True}}


class MovieSerializer(serializers.ModelSerializer):
    poster_links = serializers.SerializerMethodField(source='posters')

    class Meta:
        model = Movie
        exclude = ('slug',)
        read_only_fields = ('id', 'created_at', 'updated_at')

    @extend_schema_field({
        "type": "array",
        "items": {"type": "string", "format": "uri"}
    })
    def get_poster_links(self, obj):
        request = self.context.get('request')
        posters = obj.posters.all()
        posters_url = [request.build_absolute_uri(image.poster.url) for image in posters]
        return posters_url
