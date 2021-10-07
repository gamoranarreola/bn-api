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
    StaffAssignment,
    StaffLine,
    WorkOrder
)


class UserCreateSerializer(BaseUserRegistrationSerializer):

    class Meta:
        model = AuthUser

        fields = [
            'first_name',
            'last_name',
            'email',
            'password'
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):

        if self.initial_data['password'] != self.initial_data['password_confirm']:
            return False

        user = AuthUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            is_active=False
        )

        user.set_password(self.validated_data['password'])
        user.save()

        profile = CustomerProfile(
            auth_user =  user,
            customer_profile_id = f'C{user.id * 2 + 100}',
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
            'id',
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

    auth_user = AuthUserSerializer(read_only=True)
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


class ServiceSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(read_only=True)
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


class ServiceCategorySerializer(serializers.ModelSerializer):

    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceCategory

        fields = [
            'id',
            'name',
            'panel',
            'services'
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


class StaffLineSerializer(serializers.ModelSerializer):

    staff_assignment = serializers.PrimaryKeyRelatedField(read_only=False, queryset=StaffAssignment.objects.all())
    auth_user = serializers.PrimaryKeyRelatedField(queryset=AuthUser.objects.all())

    class Meta:
        model = StaffLine

        fields = [
            'id',
            'auth_user',
            'pay_out',
            'staff_assignment'
        ]

class StaffAssigmentSerializer(serializers.ModelSerializer):

    line_item = serializers.PrimaryKeyRelatedField(many=False, queryset=LineItem.objects.all())
    staff_lines = StaffLineSerializer(many=True, read_only=True)

    class Meta:
        model = StaffAssignment

        fields = [
            'id',
            'line_item',
            'index',
            'staff_lines'
        ]


class LineItemSerializer(serializers.ModelSerializer):

    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Service.objects.all(), source='service')
    staffing_assignments = StaffAssigmentSerializer(many=True, read_only=True)

    class Meta:
        model = LineItem

        fields = [
            'id',
            'service',
            'service_id',
            'service_date',
            'service_time',
            'quantity',
            'price',
            'staffing_assignments',
        ]

        optional_fields = ['service_id']


class WorkOrderSerializer(serializers.ModelSerializer):

    line_items = LineItemSerializer(many=True, read_only=True)
    notes = serializers.CharField(allow_blank=True)
    customer_profile = CustomerProfileSerializer(read_only=True)
    customer_profile_id = serializers.PrimaryKeyRelatedField(many=False, queryset=CustomerProfile.objects.all(), source='customer_profile')

    class Meta:
        model = WorkOrder

        fields = [
            'id',
            'request_date',
            'request_time',
            'customer_profile',
            'customer_profile_id',
            'place_id',
            'notes',
            'line_items',
            'status',
            'payment_id',
        ]

        optional_fields = ['customer_profile_id']
