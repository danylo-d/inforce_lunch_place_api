import datetime
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from lunch_app.models import Restaurant, Menu
from lunch_app.serializers import VotingResultSerializer

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def restaurant():
    return Restaurant.objects.create(name="Test Restaurant")


@pytest.fixture
def menu(restaurant):
    return Menu.objects.create(
        restaurant=restaurant,
        date=datetime.date.today(),
        items="Item 1, Item 2, Item 3",
    )


@pytest.mark.django_db
def test_menu_create(api_client, restaurant, user):
    api_client.force_authenticate(user=user)
    data = {
        "restaurant": restaurant.id,
        "date": datetime.date.today(),
        "items": "Item 1, Item 2, Item 3",
    }
    response = api_client.post("/api/menus/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Menu.objects.count() == 1
    assert Menu.objects.get().restaurant == restaurant


@pytest.mark.django_db
def test_menu_vote(api_client, menu, user):
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/api/menus/{menu.id}/vote/")
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert menu.voters.count() == 1
    assert menu.voters.first() == user


@pytest.mark.django_db
def test_menu_voting_results(api_client, menu, user):
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/menus/voting-results/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    serializer = VotingResultSerializer(instance=menu)
    assert response.data[0] == serializer.data


@pytest.mark.django_db
def test_menu_today_menu(api_client, menu, user):
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/menus/today-menu/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    serializer = VotingResultSerializer(instance=menu)
    assert response.data[0] == serializer.data


@pytest.mark.django_db
def test_menu_vote_already_voted(api_client, menu, user):
    menu.voters.add(user)
    api_client.force_authenticate(user=user)
    response = api_client.post(f"/api/menus/{menu.id}/vote/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == "You have already voted for this menu"
