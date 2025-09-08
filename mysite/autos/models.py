from django.db import models
from django.contrib.auth.models import User


class Make(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


class Auto(models.Model):
    nickname = models.CharField(max_length=200)
    mileage = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nickname
