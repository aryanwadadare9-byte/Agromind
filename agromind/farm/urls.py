from django.urls import path
from . import views

urlpatterns = [
    path("", views.farm_home, name="farm"),
    path("setup/", views.farm_setup, name="farm_setup"),
    path("add-crop/", views.add_crop, name="add_crop"),
    path("delete-crop/<int:pk>/", views.delete_crop, name="delete_crop"),
    path("add-activity/", views.add_activity, name="add_activity"),
    path("delete-activity/<int:pk>/", views.delete_activity, name="delete_activity"),
    path("add-harvest/", views.add_harvest, name="add_harvest"),
    path("add-sale/", views.add_sale, name="add_sale"),
]