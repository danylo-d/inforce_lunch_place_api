from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.versioning import AcceptHeaderVersioning

from .models import Restaurant, Menu


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_full_name(obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "full_name",
        )
        versioning_class = AcceptHeaderVersioning


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
        versioning_class = AcceptHeaderVersioning


class MenuSerializer(serializers.ModelSerializer):
    versioning_class = AcceptHeaderVersioning

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ("voters",)


class MenuListSerializer(MenuSerializer):
    class Meta:
        model = Menu
        fields = ("id", "date", "restaurant_id", "preview")


class MenuDetailSerializer(MenuSerializer):
    restaurant_name = serializers.CharField(
        source="restaurant.name",
        read_only=True
    )

    class Meta:
        model = Menu
        fields = ("id", "date", "restaurant_id", "restaurant_name", "items")


class VotingResultSerializer(MenuSerializer):
    menu_id = serializers.IntegerField(source="id", read_only=True)
    restaurant = serializers.CharField(
        source="restaurant.name",
        read_only=True
    )
    total_votes = serializers.IntegerField(
        source="voters.count",
        read_only=True
    )
    voters = UserSerializer(many=True)

    class Meta:
        model = Menu
        fields = ("menu_id", "restaurant", "items", "total_votes", "voters")
        read_only_fields = ("__all__",)


class VoteSerializer(serializers.Serializer):
    versioning_class = AcceptHeaderVersioning
