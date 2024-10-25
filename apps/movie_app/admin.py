from django.contrib import admin
from .models import MoviePoster, Movie, Showtime, MovieGenre

admin.site.register(Movie)
admin.site.register(MoviePoster)
admin.site.register(Showtime)
admin.register(MovieGenre)
