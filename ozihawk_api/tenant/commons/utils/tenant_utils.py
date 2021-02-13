from django.db import connection


class TenantUtils:
    @staticmethod
    def set_current_tenant(tenant, request):
        request.tenant = tenant
        connection.set_tenant(request.tenant)
