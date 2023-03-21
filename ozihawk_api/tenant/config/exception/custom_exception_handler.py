from ozihawk_api.commons.constants.config_constants import HTTPConstants
from tenant.commons.utils.custom_api_error_utils import CustomAPIErrorUtils
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

def handle(exc, context):
    # Call REST framework's default exception handler first, 
    # to get the standard error response.
    response = exception_handler(exc, context)

    error = None
    error_description = None

    try:
        auth_header = exc.auth_header
    except Exception:
        auth_header = None
    auth_header_array = [] if auth_header is None else auth_header.split(",")
    for header_string in auth_header_array:
        if "error_description" in header_string:
            error_description_array = header_string.split("=")
            error_description = error_description_array[1] if len(error_description_array) > 0 else None
            error_description = error_description.replace("\"", "") if error_description is not None else None
            continue

        if "error" in header_string:
            error_array = header_string.split("=")
            error = error_array[1] if len(error_array) > 0 else None
            error = error.replace("\"", "") if error is not None else None

    # Now add the HTTP status code to the response.
    if response is not None:
        if response.reason_phrase == HTTPConstants.ERROR_RESPONSE_REASON_PHRASE_UNAUTHORIZED:
            response = Response(
                data=CustomAPIErrorUtils.create(
                    message="You are not authorized",
                    description=error_description\
                        if error == "invalid_token" else "You are not authorized for this action"
                ),
                content_type="application/json",
                status=status.HTTP_401_UNAUTHORIZED
            )
    else:
        response = Response(
            data=CustomAPIErrorUtils.create(
                message="Internal Server Error",
                description="Some internal error, please try again or contact administrator"
            ),
            content_type="application/json",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response