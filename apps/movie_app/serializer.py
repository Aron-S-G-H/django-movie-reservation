from rest_framework import serializers
from .models import MovieGenre, Movie, Showtime, Seat, Reservation
from drf_spectacular.utils import extend_schema_field


class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGenre
        exclude = ('created_at', 'updated_at')
        read_only_fields = ('id', 'slug')
        extra_kwargs = {'description': {'required': True}}


class MovieShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = ('id', 'show_date', 'start_time')


class MovieSerializer(serializers.ModelSerializer):
    poster_links = serializers.SerializerMethodField(source='posters')
    show_times = MovieShowtimeSerializer(many=True, source='showtimes')

    class Meta:
        model = Movie
        exclude = ('created_at', 'updated_at')
        read_only_fields = ('id', 'slug')

    @extend_schema_field({
        "type": "array",
        "items": {"type": "string", "format": "uri"}
    })
    def get_poster_links(self, obj):
        request = self.context.get('request')
        posters = obj.posters.all()
        posters_url = [request.build_absolute_uri(image.poster.url) for image in posters]
        return posters_url


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number']


class ReservationSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(slug_field='title', read_only=True)
    user = serializers.SerializerMethodField()
    seats = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    showtime = MovieShowtimeSerializer()

    class Meta:
        model = Reservation
        exclude = ('created_at', 'updated_at')

    @extend_schema_field(
        {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'full_name': {'type': 'string'}
            }
        }
    )
    def get_user(self, obj):
        return {'id': obj.user.id, 'full_name': obj.user.get_full_name()}


class ReservationCreateSerializer(serializers.Serializer):
    showtime_id = serializers.IntegerField(required=True, help_text="Showtime ID")
    seats = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text="List of seat IDs"
    )
