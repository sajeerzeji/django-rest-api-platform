from django.core.exceptions import ObjectDoesNotExist
from oauthlib.oauth2.rfc6749.grant_types.base import GrantTypeBase
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User

from ozihawk_api.commons.constants.tenant_constants import TenantConstants
from ozihawk_api.commons.utils.db_utils import DBUtils
from ozihawk_api.commons.utils.number_utils import NumberUtils
from tenant.commons.utils.tenant_api_responses import TenantAPIErrors
from tenant.commons.utils.tenant_utils import TenantUtils
from tenant.persistence.model.tenant_model import Tenant
from tenant.serializers.tenant.tenant_serializer import TenantSerializer


class TenantView(GrantTypeBase, viewsets.ViewSet):
    # authentication_classes = ([])
    permission_classes = (IsAdminUser,)
    serializer_class = TenantSerializer

    def get(self, request, *args, **kwargs):
        # request_validator = request_validator or RequestValidator()
        # request_validator.authenticate_client(request)
        # validator = OAuth2Validator()
        # validator.authenticate_client(request)
        tenantName = request.GET['tenant']
        if tenantName is None:
            raise APIException('A tenant name is mandatory')
        try:
            tenant = Tenant.objects.get(tenant_name=tenantName)
        except ObjectDoesNotExist:
            tenant = None
        if tenant is None:
            raise APIException('Tenant' + (' ' + tenantName if tenantName is not None else '') + ' does not exists')
        serializer = self.serializer_class(tenant, many=False)
        tenant = serializer.data
        if tenant is not None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # request_validator = RequestValidator()
        # request_validator.authenticate_client(request)
        # auth_response = OAuth2Validator().authenticate_client(request)
        # if not auth_response:
        #     return Response({"error": "invalid_client"}, status=status.HTTP_200_OK)
        client = request.data or {}
        tenant_name = client.get("tenant")
        super_user_username = client.get("username")
        super_user_password = client.get("password")
        super_user_first_name = client.get("firstName")
        super_user_last_name = client.get("lastName")
        super_user_email = client.get("email")
        super_user_mobile = client.get("mobile")
        if tenant_name is None:
            raise APIException(TenantAPIErrors.API_ERROR_TENANT_NAME_EMPTY.get("message"))
        if super_user_username is None:
            raise APIException(TenantAPIErrors.API_ERROR_USERNAME_EMPTY.get("message"))
        if super_user_password is None:
            raise APIException(TenantAPIErrors.API_ERROR_PASSWORD_EMPTY.get("message"))
        if super_user_first_name is None:
            raise APIException(TenantAPIErrors.API_ERROR_FIRST_NAME_EMPTY.get("message"))
        if super_user_last_name is None:
            raise APIException(TenantAPIErrors.API_ERROR_LAST_NAME_EMPTY.get("message"))
        if super_user_email is None:
            raise APIException(TenantAPIErrors.API_ERROR_EMAIL_EMPTY.get("message"))
        if super_user_mobile is None:
            raise APIException(TenantAPIErrors.API_ERROR_MOBILE_EMPTY.get("message"))

        try:
            tenant_to_check = Tenant.objects.get(tenant_name=tenant_name)
        except ObjectDoesNotExist as ex:
            tenant_to_check = None

        if tenant_to_check is not None:
            raise APIException("Tenant already exists")

        latest_tenant = None
        schema_name = TenantConstants.TENANT_SCHEMA_NAME_PREFIX + TenantConstants.DEFAULT_TENANT_ID
        try:
            latest_tenant = Tenant.objects\
                .filter(schema_name__contains=TenantConstants.TENANT_SCHEMA_NAME_PREFIX).latest("schema_name")
        except Exception as ex:
            default_tenant = DBUtils.get_or_none(self, Tenant, schema_name=schema_name)
            if default_tenant is not None:
                raise APIException("Please Try Again")

        if latest_tenant is not None:
            latest_schema_name = latest_tenant.schema_name
            if TenantConstants.TENANT_SCHEMA_NAME_PREFIX in latest_schema_name:
                latest_schema_id = NumberUtils.int_or_0(
                    latest_schema_name.replace(TenantConstants.TENANT_SCHEMA_NAME_PREFIX, "")
                )
                if latest_schema_id == 0:
                    raise APIException("Please Try Again")
                schema_name = TenantConstants.TENANT_SCHEMA_NAME_PREFIX + str(latest_schema_id + 1)
            else:
                raise APIException("Please Try Again")


        tenant_data = {}
        tenant_data["tenant_name"] = tenant_name
        tenant_data["schema_name"] = schema_name

        try:
            tenant = Tenant.objects.create(**tenant_data)
            tenant.save()
        except Exception as ex:
            raise APIException("Couldn't create tenant")

        TenantUtils.set_current_tenant(tenant, request)

        try:
            # tenant_level_tenant = Tenant.objects.create(**tenant_data)
            # tenant_level_tenant.save()
            user = User.objects.create_user(super_user_username, email=super_user_email,
                                            password=super_user_password, first_name=super_user_first_name,
                                            last_name=super_user_last_name, is_staff=False, is_superuser=True)
        except Exception as ex:
            raise APIException("Couldn't create user")

        serializer = self.serializer_class(tenant, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)