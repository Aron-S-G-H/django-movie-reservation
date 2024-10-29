from . import views
from rest_framework.routers import SimpleRouter

app_name = 'movie'

router = SimpleRouter()
router.register('', views.MovieViewSet, basename='movie')
router.register('genre', views.MovieGenreViewSet, basename='genre')
router.register('showtimes', views.ShowTimeViewSet, basename='showtimes')

urlpatterns = router.urls
