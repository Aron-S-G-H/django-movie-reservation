from django.contrib import admin
from .models import MoviePoster, Movie

# Register your models here.
admin.site.register(Movie)
admin.site.register(MoviePoster)
