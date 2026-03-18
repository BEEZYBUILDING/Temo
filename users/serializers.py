from rest_framework import serializers
from .models import CustomUser, Address

class RegisterSerializer(serializers.ModelSerializer): #for creating users
    #Modelserializer is for when building a serializer that closely maps to an existing django model
    password = serializers.CharField(write_only=True, min_length=8)
        #write_only : nh is accepted in the request but never returned in the response
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
    #ordinary serializer ids for when handling data that does not correspond directly to a django model
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
        
class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    #address = Address.objects.filter(validated_data).exclude(id=address.id)
    
    class Meta:
        model = Address
        fields = ['user', 'full_name', 'phone',
                  'street', 'city', 'state', 
                  'country', 'postal_code', 'is_default']
        
    def create(self, validated_data):
        if validated_data.get('is_default'):
            Address.objects.filter(user=validated_data['user']).update(is_default=False)
        address = Address.objects.create(**validated_data)
        return address
    
    def update(self, instance, validated_data):
        # instance-existing adress objects fetched from the database
        #validated_data-the new_data sent in the request
        if validated_data.get('is_default'):
            Address.objects.filter(user=instance.user).update(is_default=False)
        #checks for the new data sent, if ti cant find it it uses the leaves the former one
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.street  = validated_data.get('street', instance.street )
        instance.city  = validated_data.get('city', instance.city )
        instance.state  = validated_data.get('state', instance.state )
        instance.country  = validated_data.get('country', instance.country )
        instance.postal_code  = validated_data.get('postal_code', instance.postal_code )
        
        instance.is_default = validated_data.get('is_default', instance.is_default)
        instance.save()
        return instance
    
class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone_number', 'email', 'role']
    
    
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    
    
    

    """
     the view's job is to receive the request and return a response. 
     The serializer's job is to handle data validation and saving.
    """