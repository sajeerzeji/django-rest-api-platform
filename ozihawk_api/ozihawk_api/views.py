import rest_framework
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from oauth2_provider.settings import DEFAULTS, IMPORT_STRINGS, MANDATORY, OAuth2ProviderSettings, USER_SETTINGS
from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.views.base import TokenView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from django.db import connection
import json
import logging

from oauthlib.oauth2 import RequestValidator
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from django.http.response import HttpResponse
import jwt
import base64
from oauth2_provider.views.mixins import OAuthLibMixin
from tenant_schemas import utils

from ozihawk_api.commons.utils.JWTUtils import JWTUtils
from tenant.commons.utils import tenant_api_responses
from tenant.commons.utils.tenant_api_responses import TenantAPIErrors
from tenant.commons.utils.tenant_utils import TenantUtils
from tenant.persistence.model.tenant_model import Tenant

log = logging.getLogger(__name__)


class CustomTokenView(TokenView):
    valid_http_request_methods = ('POST',)

    def __init__(self):
        self._valid_http_request_methods = None

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        tenant_name = request.GET.get("tenant");
        if tenant_name is None:
            raise APIException('A tenant name is mandatory.')
        try:
            tenant = Tenant.objects.get(tenant_name=tenant_name)
        except ObjectDoesNotExist as ex:
            raise APIException(TenantAPIErrors.API_ERROR_TENANT_NOT_FOUND["message"])

        if tenant is not None:
            """ TENANT AWARE - START """
            TenantUtils.set_current_tenant(tenant, request)
            """ TENANT AWARE - END """
            url, headers, body, status = self.create_token_response(request)
            if status == 200:
                body = json.loads(body)
                access_token = body.get("access_token")
                refresh_token = body.get("refresh_token")
                if access_token is not None:
                    token = get_access_token_model().objects.get(token=access_token)
                    # token = jwt.encode({'token': token}, '0VYVGEHMlXDDsdKloKKyHVr8e5slQd7r', algorithm='HS256')
                    app_authorized.send(
                        sender=self, request=request,
                        token=token)
                    access_token_object = {
                        "token": access_token,
                        "tenant": tenant_name,
                        "user": {
                            "username": token.user.username,
                            "email": token.user.email
                        }
                    }
                    refresh_token_object = {
                        "token": refresh_token
                    }
                    body["access_token"] = JWTUtils.encode_access_token(payload=access_token_object)
                    body["refresh_token"] = JWTUtils.encode_refresh_token(payload=refresh_token_object)
                    body = json.dumps(body)
            response = HttpResponse(content=body, status=status)
            for k, v in headers.items():
                response[k] = v
        else:
            raise APIException(TenantAPIErrors.API_ERROR_TENANT_NOT_FOUND["message"])
        return response

@method_decorator(csrf_exempt, name="dispatch")
class CustomRevokeTokenView(OAuthLibMixin, View):
    """
    Implements an endpoint to revoke access or refresh tokens
    """
    oauth2_settings = OAuth2ProviderSettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS, MANDATORY)
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_revocation_response(request)
        response = HttpResponse(content=body or "", status=status)

        for k, v in headers.items():
            response[k] = v
        return response


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')
