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
from django.core.mail import send_mail

class MyUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.AllowAny]
    
    def send_email(self):
        try:
            send_mail(
                    subject=EMAIL_SUBJECT,
                    message=EMAIL_MESSAGE,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.SERVER_EMAIL],
                    fail_silently=True,
                )
        except ExternalAPIError as e:
            raise ExternalAPIError (
                detail= EMAIL_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve_status(self,pk):
        if pk%2==0:
            return 'active'
        return 'inactive'
      
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
            user.status = self.retrieve_status(user.id)
            
            if(user.status=='inactive'):
                print("mail enviado")
                self.send_email()
            
            return Response(serializer.data)
            
        except Http404:
            raise ExternalAPIError(detail=USER_NOT_FOUND, code=status.HTTP_404_NOT_FOUND)
        
        except requests.exceptions.RequestException:
            raise ExternalAPIError()