from os import read
from rest_framework import serializers

from .models import (
    AuthUser,
    CustomerProfile,
    CustomerProfileAddress,
    BeautierProfile,
    Region,
    ServicePublicPrice,
    Specialty,
    ServiceCategory,
    Service,
    LineItem,
    StaffAssignment,
    StaffLine,
    WorkOrder
)


class UserCreateSerializer():

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


class ServiceCategorySerializer(serializers.ModelSerializer):

    services = serializers.SerializerMethodField()

    class Meta:
        model = ServiceCategory

        fields = [
            'id',
            'name',
            'panel',
            'services',
            'active',
            'order',
        ]

    def get_services(self, instance):
        services = instance.services.filter(active=True).order_by('order')
        return ServiceSerializer(services, many=True, context=self.context).data


class ServiceSerializer(serializers.ModelSerializer):

    specialties = SpecialtySerializer(many=True, read_only=True)
    description = serializers.CharField(allow_blank=True)
    public_price = serializers.SerializerMethodField()

    class Meta:

        model = Service

        fields = [
            'id',
            'service_id',
            'name',
            'description',
            'includes_eyelashes',
            'availability',
            'duration',
            'specialties',
            'active',
            'order',
            'public_price',
        ]

    def get_public_price(self, instance):

        region_split = self.context.get('region').split('-')

        return ServicePublicPrice.objects.get(
            region_id=Region.objects.get(
                code=region_split[0],
                state_province_code=region_split[1],
                country_code=region_split[2]
            ).id,
            service_id=instance.id
        ).public_price


class RegionSerializer(serializers.ModelSerializer):

    class Meta:

        model = Region

        fields = [
            'display_name',
            'code',
            'state_province_code',
            'country_code',
        ]

class BeautierProfileSerializer(serializers.ModelSerializer):

    auth_user = AuthUserSerializer()
    specialties = SpecialtySerializer(many=True, read_only=True)

    class Meta:
        model = BeautierProfile

        fields = [
            'id',
            'auth_user',
            'specialties',
            'bio',
            'photo_url',
            'title',
            'preferred_name'
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
            'address',
            'notes',
            'line_items',
            'status',
            'payment_id',
        ]

        optional_fields = ['customer_profile_id']
