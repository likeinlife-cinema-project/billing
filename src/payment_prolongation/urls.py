from django.urls import path

from .views import StartProlongation

urlpatterns = [
    path("prolongation/", StartProlongation.as_view()),
]
