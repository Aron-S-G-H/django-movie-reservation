from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .serializer import MovieGenreSerializer, MovieSerializer, SeatSerializer, ReservationSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.decorators import action
from django.core.validators import ValidationError
from django.utils import timezone
from.models import MovieGenre, Movie, Showtime, Seat, Reservation


@extend_schema(request=MovieGenreSerializer, responses=MovieGenreSerializer, tags=['Movie Genre'])
class MovieGenreViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

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
            return Response({'response': 'Updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = get_object_or_404(MovieGenre, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({'response': 'Deleted successfully'}, status=status.HTTP_200_OK)


@extend_schema(request=MovieSerializer, responses=MovieSerializer, tags=['Movie'])
class MovieViewSet(ViewSet):
    # permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def list(self, request):
        queryset = Movie.objects.all()
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(queryset, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'response': 'Created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        instance = get_object_or_404(Movie, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = MovieSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response({'response': 'Updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = get_object_or_404(Movie, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({'response': 'Deleted successfully'}, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='date',
                type=OpenApiTypes.DATE,
                required=True,
                location=OpenApiParameter.QUERY,
                description="Date to filter movies with showtimes",
            )
        ],
    )
    @action(methods=['GET'], url_path='showtime', url_name='showtime', detail=False)
    def get_movie_with_showtimes(self, request):
        date = request.query_params.get('date', None)
        if date:
            try:
                movies = Movie.objects.filter(showtimes__show_date=date).distinct()
                serializer = MovieSerializer(movies, many=True, context={'request': request})
                return Response(serializer.data)
            except ValidationError:
                pass
        return Response(
            {"error": "Please provide a valid date in the format YYYY-MM-DD"},
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(tags=['ShowTime'])
class ShowTimeViewSet(ViewSet):
    @action(detail=True, methods=['GET'], url_path='available_seats', url_name='available_seat')
    def available_seats(self, request, pk=None):
        showtime = get_object_or_404(Showtime, pk=pk)
        available_seats = Seat.objects.filter(showtime=showtime, is_reserved=False)
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Reservation'], responses=ReservationSerializer)
class ReservationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Reservation.objects.all()
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        showtime_id = request.data.get('showtime', None)
        seat_ids = request.data.get('seats', [])

        if not showtime_id:
            return Response({'error': 'At least a showtime must be selected'}, status=status.HTTP_400_BAD_REQUEST)
        if not seat_ids:
            return Response({"error": "At least one seat must be selected."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            showtime = Showtime.objects.get(id=showtime_id)
        except Showtime.DoesNotExist:
            return Response({'error': f'showtime with id {showtime_id} does not exists'})

        reservation = Reservation.objects.create(
            user=request.user,
            movie=showtime.movie,
            showtime=showtime,
        )
        for seat_id in seat_ids:
            try:
                seat = Seat.objects.get(id=seat_id)
                seat.is_reserved = True
                seat.save()
            except Seat.DoesNotExist:
                return Response({'error': f'seat with id {seat_id} does not exists'})
            reservation.seats.add(seat)

        serializer = ReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['DELETE'], url_path='cancel', url_name='cancel_reservation', detail=False)
    def cancel_reservation(self, request, pk=None):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

        if reservation.showtime.show_date < timezone.now().date():
            return Response({"error": "Cannot cancel a reservation for a past showtime."},
                            status=status.HTTP_400_BAD_REQUEST)

        for seat in reservation.seats.all():
            seat.is_reserved = False
            seat.save()

        reservation.delete()

        return Response({"message": "Reservation canceled successfully."}, status=status.HTTP_204_NO_CONTENT)
