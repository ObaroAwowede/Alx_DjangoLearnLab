from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ('id','username','email')
        read_only_fields = ('id')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name')
        read_only_fields = ('id', 'username') 

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data["username"],
            email = validated_data.get("email"),
            password = validated_data["password"] 
        )
        
        Token.objects.create(user = user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")