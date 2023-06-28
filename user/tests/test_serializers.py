import pytest
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer

User = get_user_model()


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "password": "testpassword",
        "first_name": "John",
        "last_name": "Doe",
    }


@pytest.mark.django_db
def test_user_serializer_create(user_data):
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.username == "testuser"


@pytest.mark.django_db
def test_user_serializer_update(user_data):
    user = User.objects.create_user(**user_data)

    updated_data = user_data.copy()
    updated_data["first_name"] = "Updated First Name"

    serializer = UserSerializer(instance=user, data=updated_data, partial=True)
    assert serializer.is_valid()
    updated_user = serializer.save()
    assert updated_user.first_name == "Updated First Name"
