from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'age']

    def validate_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise serializers.ValidationError('Name must be a non-empty string.')
        return value.strip()

    def validate_age(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError('Age must be an integer.')
        if value < 0 or value > 120:
            raise serializers.ValidationError('Age must be between 0 and 120.')
        return value

