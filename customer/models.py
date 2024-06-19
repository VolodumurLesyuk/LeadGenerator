from django.contrib.auth.models import User
from django.db import models

import uuid


class Customer(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.login)