from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
urlpatterns = [
    path("", lambda r: redirect("farm")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("farm/", include("farm.urls")),
    path("disease/", include("disease.urls")),
    path("market/", include("market.urls")),
    path("organic/", include("organic.urls")),
    path("rainfall/", include("rainfall.urls")),
    path("news/", include("news.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
