from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("lunch_app.urls", namespace="lunch_app")),
    path("api/user/", include("user.urls", namespace="user")),
]
