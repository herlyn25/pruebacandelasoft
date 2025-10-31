from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from .constants import ERROR_CONNECTION_TO_EXTERNAL_API

class ExternalAPIError(APIException):
    """
    General Exception to build error messages.
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = ERROR_CONNECTION_TO_EXTERNAL_API
    
    def __init__(self, detail=None, code =None):
        """
        detail: Error message (optional)
        code: Customized code (optional)
        """
        if detail is not None:
            self.detail="Nuevo detalle"

        # Call to original constructor from APIException
        super().__init__(detail=detail, code=code )
        
        if code is not None:
            self.status_code=code 