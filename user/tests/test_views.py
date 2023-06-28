import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def authenticated_user(api_client, user_data):
    user = User.objects.create_user(**user_data)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return user


@pytest.mark.django_db
def test_create_user(api_client, user_data):
    response = api_client.post("/api/user/register/", user_data, format="json")
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.first().username == user_data["username"]


@pytest.mark.django_db
def test_manage_user_view(authenticated_user, api_client):
    response = api_client.get("/api/user/me/")
    assert response.status_code == 200
    assert response.data["username"] == authenticated_user.username


# Add more test cases for other custom methods in the views as needed


@pytest.mark.django_db
def test_user_serializer_create():
    serializer = UserSerializer(
        data={
            "username": "testuser",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }
    )
    assert serializer.is_valid()
    user = serializer.save()
    assert User.objects.count() == 1
    assert User.objects.first().username == user.username


@pytest.mark.django_db
def test_user_serializer_update(authenticated_user):
    serializer = UserSerializer(
        instance=authenticated_user,
        data={"first_name": "Updated"},
        partial=True
    )
    assert serializer.is_valid()
    serializer.save()
    assert User.objects.first().first_name == "Updated"
