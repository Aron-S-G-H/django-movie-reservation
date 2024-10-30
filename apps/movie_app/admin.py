from django.contrib import admin
from .models import MoviePoster, Movie, Showtime, MovieGenre, Seat, Reservation

# Register your models here.
admin.site.register(Movie)
admin.site.register(MoviePoster)
admin.site.register(Showtime)
admin.site.register(Seat)
admin.site.register(Reservation)
admin.site.register(MovieGenre)
