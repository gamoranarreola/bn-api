from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from beauty_now.bn_app.models import (
    CustomUser,
    CustomerProfile,
    CustomerProfileAddress,
    BeautierProfile,
    BeautierProfileSpecialty,
    Specialty,
    ServiceCategory,
    Service,
    LineItem,
    WorkOrder
)


class UserCreateSerializer(BaseUserRegistrationSerializer):

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

    class Meta:
        model = CustomUser

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


class BeautierProfilesSpecialtiesSerializer(serializers.ModelSerializer):

    specialty = SpecialtySerializer()

    class Meta:
        model = BeautierProfileSpecialty

        fields = [
            'specialty'
        ]


class BeautierProfileSerializer(serializers.ModelSerializer):

    custom_user = CustomUserSerializer()
    specialties = SpecialtySerializer(many=True, read_only=True)

    class Meta:
        model = BeautierProfile

        fields = [
            'id',
            'custom_user',
            'calendar_id',
            'specialties',
            'availability'
        ]


class LineItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = LineItem

        fields = [
            'id',
            'service',
            'service_date',
            'service_time',
            'quantity',
            'price',
            'beautier_profile',
        ]


class WorkOrderSerializer(serializers.ModelSerializer):

    line_items = LineItemSerializer(many=True)
    notes = serializers.CharField(allow_blank=True)

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

    def create(self, validated_data):

        line_items_data = validated_data.pop('line_items')
        work_order = WorkOrder.objects.create(**validated_data)

        for line_item in line_items_data:
            LineItem.objects.create(work_order=work_order, **line_item)

        return work_order
