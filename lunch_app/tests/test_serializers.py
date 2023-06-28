import pytest
from django.contrib.auth import get_user_model
from datetime import date
from lunch_app.models import Restaurant, Menu
from lunch_app.serializers import (
    UserSerializer,
    RestaurantSerializer,
    MenuSerializer,
    VotingResultSerializer,
    VoteSerializer,
    MenuDetailSerializer,
    MenuListSerializer,
)

User = get_user_model()


@pytest.fixture
def restaurant():
    return Restaurant(name="Test Restaurant")


@pytest.fixture
def menu(restaurant):
    return Menu(
        restaurant=restaurant,
        date=date.today(),
        items="Item 1, Item 2, Item 3",
    )


def test_user_serializer_get_full_name():
    user = User(first_name="John", last_name="Doe")
    serializer = UserSerializer(instance=user)
    assert serializer.data["full_name"] == "John Doe"


def test_restaurant_serializer():
    restaurant = Restaurant(name="Test Restaurant")
    serializer = RestaurantSerializer(instance=restaurant)
    assert serializer.data["name"] == "Test Restaurant"


def test_menu_serializer():
    restaurant = Restaurant(name="Test Restaurant")
    menu = Menu(
        restaurant=restaurant,
        date=date.today(),
        items="Item 1, Item 2, Item 3"
    )
    serializer = MenuSerializer(instance=menu)
    assert serializer.data["items"] == "Item 1, Item 2, Item 3"


def test_vote_serializer():
    serializer = VoteSerializer(data={"example": "data"})
    assert serializer.is_valid()


def test_menu_detail_serializer():
    restaurant = Restaurant(name="Test Restaurant")
    menu = Menu(
        restaurant=restaurant,
        date=date.today(),
        items="Item 1, Item 2, Item 3"
    )
    serializer = MenuDetailSerializer(instance=menu)
    assert serializer.data["restaurant_name"] == "Test Restaurant"


def test_menu_list_serializer():
    restaurant = Restaurant(name="Test Restaurant")
    menu = Menu(
        restaurant=restaurant,
        date=date.today(),
        items="Item 1, Item 2, Item 3"
    )
    serializer = MenuListSerializer(instance=menu)
    assert serializer.data["preview"] == "Item 1, Item 2, Item"
