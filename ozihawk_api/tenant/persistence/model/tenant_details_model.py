from django.db import models

from tenant.persistence.model.user_model import User


class TenantDetails:
    name = models.CharField(max_length=500, unique=True, null=False, blank=False)
    type = models.CharField(max_length=100, unique=True, null=False, blank=False)
    app = models.CharField(max_length=200, unique=True, null=False, blank=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile: models.CharField(max_length=10, unique=True, null=False, blank=False)
    address: models.CharField(max_length=250, unique=True, null=False, blank=False)
    street: models.CharField(max_length=100, unique=True, null=False, blank=False)
    city: models.CharField(max_length=100, unique=True, null=False, blank=False)
    state: models.CharField(max_length=100, unique=True, null=False, blank=False)
    country: models.CharField(max_length=100, unique=True, null=False, blank=False)
    zip: models.CharField(max_length=10, unique=True, null=False, blank=False)