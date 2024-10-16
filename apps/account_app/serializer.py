from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from .utils import validate_and_format_phone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ('user_permissions', 'groups')
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=128, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    def validate_phone(self, value):
        try:
            phone = validate_and_format_phone(phone_number=value)
        except Exception as e:
            raise serializers.ValidationError(e)
        return phone

    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('First name must contain only alphabetic characters')
        return value

    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Last name must contain only alphabetic characters')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password fields didnt match'})

        allowed_fields = set(self.fields)
        received_fields = set(self.initial_data.keys())
        invalid_fields = received_fields - allowed_fields
        if invalid_fields:
            raise serializers.ValidationError(f"Invalid fields: {', '.join(invalid_fields)}")

        return attrs


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_phone(self, value):
        try:
            phone = validate_and_format_phone(phone_number=value)
        except Exception as e:
            raise serializers.ValidationError(e)
        return phone

    def validate(self, data):
        allowed_fields = set(self.fields)
        received_fields = set(self.initial_data.keys())
        invalid_fields = received_fields - allowed_fields
        if invalid_fields:
            raise serializers.ValidationError(f"Invalid fields: {', '.join(invalid_fields)}")

        user = authenticate(phone=data['phone'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid phone or password")

        return user
