from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers

from ..models.user_models import CustomUser
from ..models.customer_profile_models import CustomerProfile, CustomerProfileAddress


class UserCreateSerializer(BaseUserRegistrationSerializer):
    """
    User create serializer.

    Arguments:
        serializers {ModelSerializer} -- ModelSerializer class.
    """
    class Meta:
        model = CustomUser

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'password'
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        """
        Create method.
        
        Arguments:
            validated_data {dict} -- Validated for custom user.
        
        Returns:
            CustomUser -- Custom user record.
        """
        user = CustomUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            is_active=False
        )

        user.set_password(self.validated_data['password'])
        user.save()
    
        profile = CustomerProfile(       
            custom_user =  user,    
            customer_id = f'C{user.id * 2 + 100}',
        )

        profile.save();

        return user


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Custom user serializer.
    """
    class Meta:
        model = CustomUser

        fields = [
            'first_name',
            'last_name'
        ]


class CustomerProfileAddressSerializer(serializers.ModelSerializer):
    """
    CustomerProfileAddress serializer.
    """
    class Meta:
        model = CustomerProfileAddress

        fields = [
            'id',
            'customer_profile',
            'place_id',
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):

    custom_user = CustomUserSerializer()
    addresses = CustomerProfileAddressSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerProfile

        fields = [
            'id',
            'custom_user',
            'customer_profile_id',
            'addresses'     
        ]
