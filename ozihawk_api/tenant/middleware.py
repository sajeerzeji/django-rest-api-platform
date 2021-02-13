from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from tenant_schemas.middleware import BaseTenantMiddleware
from tenant_schemas.utils import get_public_schema_name

from ozihawk_api.commons.constants.tenant_constants import TenantConstants
from ozihawk_api.commons.utils.JWTUtils import JWTUtils


class RequestIDTenantMiddleware(BaseTenantMiddleware):

    def get_tenant(self, model, hostname, request):
        try:
            schema = model.objects.get(
                schema_name=get_public_schema_name()
            )
        except ObjectDoesNotExist as ex:
            schema = model.objects.create(
                domain_url=hostname,
                schema_name=get_public_schema_name(),
                tenant_name=TenantConstants.DEFAULT_TENANT_NAME
            )
            schema.save()
        authentication = request.META.get('HTTP_AUTHORIZATION')
        if authentication is not None and "Bearer " in authentication:
            tenant = JWTUtils.decode_access_token(authentication, False)
            tenant_name = tenant.get("tenant")
            schema = model.objects.get(tenant_name=tenant_name)
        return schema