from rest_framework import serializers
from .models import MyUser

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id','firstname', 'lastname', 'external_data', 'created_at')
        read_only_fields = ('external_data',  'created_at',)