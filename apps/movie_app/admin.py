from django.contrib import admin
from .models import MoviePoster, Movie

from .models import MovieGenre
# Register your models here.
admin.site.register(Movie)
admin.site.register(MoviePoster)

admin.register(MovieGenre)
