from rest_framework import serializers
from userApp.models import KeycloakUser
from django.contrib.auth import authenticate
from rest_framework import serializers

class KeycloakUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=KeycloakUser
        fields='__all__'

