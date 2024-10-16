from . import views
from rest_framework.routers import SimpleRouter

app_name = 'movie'

router = SimpleRouter()
router.register('genre', views.MovieGenreViewSet, basename='genre')

urlpatterns = router.urls
