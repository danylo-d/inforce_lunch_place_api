from django.urls import path, include
from rest_framework import routers
from lunch_app.views import RestaurantViewSet, MenuViewSet

router = routers.DefaultRouter()
router.register(r"restaurants", RestaurantViewSet, basename="restaurants")
router.register(r"menus", MenuViewSet, basename="menus")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "lunch_app"
