from . import views
from rest_framework.routers import SimpleRouter

app_name = 'account'

router = SimpleRouter()
router.register('auth', views.UserAuthenticationViewSet, basename='auth')
router.register('users', views.UserViewSet, basename='users')

urlpatterns = router.urls
