from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    date = models.DateField(auto_now_add=True)
    items = models.TextField()
    voters = models.ManyToManyField(get_user_model(), blank=True)

    @property
    def preview(self):
        return self.items[:20]

    def __str__(self):
        return f"{self.restaurant} - {self.date}"
