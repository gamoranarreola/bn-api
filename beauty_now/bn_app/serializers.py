from os import read
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from .models import (
    AuthUser,
    CustomerProfile,
    CustomerProfileAddress,
    BeautierProfile,
    Specialty,
    ServiceCategory,
    Service,
    LineItem,
    StaffingAssignment,
    WorkOrder
)


class UserCreateSerializer(BaseUserRegistrationSerializer):

    class Meta:
        model = AuthUser

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

        user = AuthUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            is_active=False
        )

        user.set_password(self.validated_data['password'])
        user.save()

        profile = CustomerProfile(
            auth_user =  user,
            customer_id = f'C{user.id * 2 + 100}',
        )

        profile.save();
        print('profile created')
        return user


class MeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone'
        ]


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser

        fields = [
            'first_name',
            'last_name'
        ]


class CustomerProfileAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerProfileAddress

        fields = [
            'id',
            'customer_profile',
            'place_id',
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):

    auth_user = AuthUserSerializer()
    addresses = CustomerProfileAddressSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerProfile

        fields = [
            'id',
            'auth_user',
            'customer_profile_id',
            'addresses'
        ]


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty

        fields = [
            'id',
            'name'
        ]


class ServiceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceCategory

        fields = [
            'id',
            'name'
        ]


class ServiceSerializer(serializers.ModelSerializer):

    category = ServiceCategorySerializer(read_only=True)
    specialties = SpecialtySerializer(many=True, read_only=True)
    description = serializers.CharField(allow_blank=True)

    class Meta:

        model = Service

        fields = [
            'id',
            'service_id',
            'category',
            'name',
            'description',
            'includes_eyelashes',
            'availability',
            'duration',
            'public_price',
            'specialties'
        ]


class BeautierProfileSerializer(serializers.ModelSerializer):

    auth_user = AuthUserSerializer()
    specialties = SpecialtySerializer(many=True, read_only=True)

    class Meta:
        model = BeautierProfile

        fields = [
            'id',
            'auth_user',
            'calendar_id',
            'specialties',
            'availability'
        ]


class StaffingAssigmentSerializer(serializers.ModelSerializer):

    lint_item = serializers.PrimaryKeyRelatedField(many=False, queryset=LineItem.objects.all())
    beautier_profiles = BeautierProfileSerializer(many=True, read_only=True)
    class Meta:
        model = StaffingAssignment

        fields = [
            'line_item',
            'index',
            'beautier_profiles',
        ]


class LineItemSerializer(serializers.ModelSerializer):

    service = serializers.PrimaryKeyRelatedField(many=False, queryset=Service.objects.all())
    staffing_assignments = StaffingAssigmentSerializer(many=True, read_only=True)
    class Meta:
        model = LineItem

        fields = [
            'id',
            'service',
            'service_date',
            'service_time',
            'quantity',
            'price',
            'staffing_assignments',
        ]


class WorkOrderSerializer(serializers.ModelSerializer):

    line_items = LineItemSerializer(many=True, read_only=True)
    notes = serializers.CharField(allow_blank=True)
    customer_profile = serializers.PrimaryKeyRelatedField(many=False, queryset=CustomerProfile.objects.all())

    class Meta:
        model = WorkOrder

        fields = [
            'id',
            'request_date',
            'request_time',
            'customer_profile',
            'place_id',
            'notes',
            'line_items',
            'status',
        ]
