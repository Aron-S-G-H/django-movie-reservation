from django.apps import AppConfig


class MovieAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.movie_app'
    verbose_name = 'movie'
