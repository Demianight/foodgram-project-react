from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UsersViewSet


router = SimpleRouter()

router.register(
    'users',
    UsersViewSet,
    'users'
)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
