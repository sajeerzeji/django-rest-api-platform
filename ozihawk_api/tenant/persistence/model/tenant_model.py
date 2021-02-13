import uuid
import os
from django.db import models
from tenant_schemas.models import TenantMixin


class Tenant(TenantMixin):
    REQUIRED_FIELDS = ('tenant_name', 'schema_name')
    tenant_name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_on = models.DateField(auto_now_add=True)
    domain_url = models.URLField(blank=True, null=True, default=os.getenv('DOMAIN'))

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    class Meta:
        db_table = "tenant"
