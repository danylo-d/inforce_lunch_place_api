import pytest
from django.contrib.auth import get_user_model
from lunch_app.models import Restaurant, Menu


@pytest.mark.django_db
def test_restaurant_model():

    restaurant = Restaurant.objects.create(name="Test Restaurant")

    saved_restaurant = Restaurant.objects.get(id=restaurant.id)

    assert saved_restaurant.name == "Test Restaurant"


@pytest.mark.django_db
def test_menu_preview():

    restaurant = Restaurant.objects.create(name="Test Restaurant")

    menu = Menu.objects.create(
        restaurant=restaurant,
        date="2023-06-28",
        items="Item 1, Item 2, Item 3, Item 4, Item 5",
    )

    assert menu.preview == "Item 1, Item 2, Item"


@pytest.mark.django_db
def test_menu_str_representation():

    restaurant = Restaurant.objects.create(name="Test Restaurant")

    menu = Menu.objects.create(
        restaurant=restaurant,
        date="2023-06-28",
        items="Item 1, Item 2, Item 3, Item 4, Item 5",
    )

    assert str(menu) == "Test Restaurant - 2023-06-28"
