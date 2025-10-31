from django.http import Http404
import requests 
from django.conf import settings
from .models import MyUser
from .serializers import MyUserSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .exceptions import ExternalAPIError
from .constants import *

class MyUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.AllowAny]
      
    def retrieve(self, request, pk=None):
        try: 
            user = self.get_object()
            serializer = self.get_serializer(user)
            external_api =f'{settings.EXTERNAL_API}/{pk}'
            external_response = requests.get(external_api, timeout=5)
                
            if external_response.status_code == 404:
                raise ExternalAPIError(
                    detail=USER_NOT_FOUND_API, 
                    code=status.HTTP_404_NOT_FOUND
                )
            external_data = external_response.json()
            filtered_data = {
                'address' : external_data.get('address'),
                'phone' : external_data.get('phone')
            }
            user.external_data = filtered_data
            return Response(serializer.data)
            
        except Http404:
            raise ExternalAPIError(detail=USER_NOT_FOUND, code=status.HTTP_404_NOT_FOUND)
        
        except requests.exceptions.RequestException:
            raise ExternalAPIError()