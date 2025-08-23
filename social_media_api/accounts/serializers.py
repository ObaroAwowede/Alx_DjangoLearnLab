from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
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
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True, label = 'Confirm Password')
    class Meta:
        model = User
        fields = ('id','username','email','password','password2')
        extra_kwargs = {"password": {"write_only": True}}
    
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        validate_password(data["password"], user=User)
        return data

    def create(self, validated_data):
        validated_data.pop("password2", None)
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username") or attrs.get("email")
        password = attrs.get("password")
        if username is None or password is None:
            raise serializers.ValidationError("Must include username/email and a password.")
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials")
        if not user.is_active:
            raise AuthenticationFailed("User is inactive")
        attrs["user"] = user
        return attrs