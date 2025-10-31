import requests 
from django.conf import settings
from .models import MyUser
from .serializers import MyUserSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

class MyUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permissions_classes = [permissions.AllowAny]
    
    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        
        try:
            external_api =f'{settings.EXTERNAL_API}/{pk}'
            external_response = requests.get(external_api, timeout=5)
            
            if external_response.status_code == 200:
                external_data = external_response.json()
                filtered_data = {
                    'address' : external_data.get('address'),
                    'phone' : external_data.get('phone')
                }
                user.external_data = filtered_data
                return Response(serializer.data)
            else:
                user.external_data = None
                return Response(serializer.data)
        
        except requests.request.RequestException as e:
            return Response({
                'error' : f'user {pk} no tiene data externa'
            })
        
        except MyUser.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
