from django.urls import include, path

from .api.urls import urlpatterns as api_urls

urlpatterns = [
    path("api/", include(api_urls)),
]
