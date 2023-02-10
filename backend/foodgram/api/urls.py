from django.urls import include, path
from rest_framework import routers

from .utils import router_data


router = routers.SimpleRouter()


for data in router_data:
    router.register(
        prefix=data.router_endpoint,
        viewset=data.viewset_class,
        basename=data.basename
    )


urlpatterns = [
    path('', include(router.urls)),
    path('', include('users.urls')),
]
