from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
        
    class Meta:
        model = CustomUser
        fields = ['email','password', 'full_name', 'phone_number']
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'unique': 'email is already registered'
                }
            }
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data, password=password)
        return user
        
class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
        