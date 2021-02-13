from tenant.model.base_model import BaseModel


class CustomException(BaseModel):
    status = str
    message = str
    description = str