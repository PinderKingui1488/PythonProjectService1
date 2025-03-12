from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("clients.urls", namespace="clients")),
    path("", include("mailings.urls", namespace="mailings")),
    path("users/", include("users.urls", namespace="users")),
]