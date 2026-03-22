from django.urls import path
from . import views
urlpatterns = [path("", views.rainfall, name="rainfall"), path("api/", views.weather_api, name="weather_api")]