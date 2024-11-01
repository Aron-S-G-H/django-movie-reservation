from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from .serializer import MovieGenreSerializer, MovieSerializer, SeatSerializer, ReservationSerializer
from .permissions import IsAdminOrReadOnly
from django.core.validators import ValidationError
from django.utils import timezone
from . import decorators
from.models import MovieGenre, Movie, Showtime, Seat, Reservation


@extend_schema(tags=['Movie Genre'])
class MovieGenreViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    @decorators.genre_list_decorator
    def list(self, request):
        queryset = MovieGenre.objects.all()
        serializer = MovieGenreSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.genre_retrieve_decorator
    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(MovieGenre, pk=pk)
        serializer = MovieGenreSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.genre_create_decorator
    def create(self, request):
        serializer = MovieGenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'response': 'Created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.genre_update_decorator
    def update(self, request, pk=None):
        instance = get_object_or_404(MovieGenre, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = MovieGenreSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response({'response': 'Updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.genre_delete_decorator
    def destroy(self, request, pk):
        instance = get_object_or_404(MovieGenre, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({'response': 'Deleted successfully'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Movie'])
class MovieViewSet(ViewSet):
    # permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    @decorators.movie_list_decorator
    def list(self, request):
        queryset = Movie.objects.all()
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.movie_retrieve_decorator
    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Movie, pk=pk)
        serializer = MovieSerializer(queryset, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.movie_create_decorator
    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'response': 'Created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.movie_update_decorator
    def update(self, request, pk=None):
        instance = get_object_or_404(Movie, pk=pk)
        self.check_object_permissions(request, instance)
        serializer = MovieSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response({'response': 'Updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.movie_delete_decorator
    def destroy(self, request, pk):
        instance = get_object_or_404(Movie, pk=pk)
        self.check_object_permissions(request, instance)
        instance.delete()
        return Response({'response': 'Deleted successfully'}, status=status.HTTP_200_OK)

    @decorators.movie_showtime_decorator
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
    @decorators.available_seats_decorator
    def available_seats(self, request, pk=None):
        showtime = get_object_or_404(Showtime, pk=pk)
        available_seats = Seat.objects.filter(showtime=showtime, is_reserved=False)
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Reservation'], responses=ReservationSerializer)
class ReservationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @decorators.reservation_list_decoration
    def list(self, request):
        queryset = Reservation.objects.all()
        serializer = ReservationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @decorators.reservation_create_decorator
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

    @decorators.reservation_cancel_decorator
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
