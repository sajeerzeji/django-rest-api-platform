from django.contrib.auth.models import User
from django.db import models


class User(User):
    mobile: models.CharField(max_length=10, unique=True, null=False, blank=False)
    address: models.CharField(max_length=250, unique=True, null=False, blank=False)
    street: models.CharField(max_length=100, unique=True, null=False, blank=False)
    city: models.CharField(max_length=100, unique=True, null=False, blank=False)
    state: models.CharField(max_length=100, unique=True, null=False, blank=False)
    country: models.CharField(max_length=100, unique=True, null=False, blank=False)
    zip: models.CharField(max_length=10, unique=True, null=False, blank=False)