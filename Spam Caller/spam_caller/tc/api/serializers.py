from django.http import request
from rest_framework import serializers
from tc.models import Phone
from django.contrib.auth.models import User

#This class doesnot introduces the email section

class PhoneSerializer(serializers.ModelSerializer):
    
    username=serializers.CharField(source="user.username", read_only=True)
    
    
    class Meta:
        model=Phone
        fields=['id', 'username','phone','is_safe']

# This serializer class introduces the email section
class PhoneSerializerReg(serializers.ModelSerializer):
    
    username=serializers.CharField(source="user.username", read_only=True)
    email=serializers.CharField(source="user.email", read_only=True)
    
    class Meta:
        model=Phone
        fields=['id', 'username','email','phone','is_safe']
        