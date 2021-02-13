from tenant.model.exception.custom_exception import CustomException
from typing import Any


class CustomAPIErrorUtils:
    
    @classmethod
    def create(cls, status = None, message=str, description=str):
        custom_exception = CustomException()
        custom_exception.status = status
        custom_exception.message = message
        custom_exception.description = description
        return custom_exception.toJSON()
