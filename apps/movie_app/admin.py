from django.contrib import admin
from .models import MoviePoster, Movie, Showtime, MovieGenre, Seat, Reservation


class MovieGenreAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'slug')
    list_display = ('name', 'description', 'slug', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    search_fields = ('name',)
    list_filter = ('is_active',)


class MoviePosterAdmin(admin.StackedInline):
    model = MoviePoster
    readonly_fields = ('poster_width', 'poster_height', 'size')
    extra = 1


class MovieShowTimeAdmin(admin.StackedInline):
    model = Showtime
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    inlines = (MoviePosterAdmin, MovieShowTimeAdmin)
    readonly_fields = ('created_at', 'updated_at', 'slug')
    list_display = ('title', 'genre', 'director', 'duration', 'release_date', 'updated_at')
    search_fields = ('title', 'director')
    list_filter = ('genre', 'language')


class SeatAdmin(admin.StackedInline):
    model = Seat
    extra = 0


class ShowTimeAdmin(admin.ModelAdmin):
    inlines = (SeatAdmin,)
    list_display = ('movie', 'show_date', 'start_time')
    list_filter = ('movie', 'show_date')


class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('user', 'movie', 'showtime', 'created_at')
    filter_horizontal = ('seats',)


# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Showtime, ShowTimeAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(MovieGenre, MovieGenreAdmin)
