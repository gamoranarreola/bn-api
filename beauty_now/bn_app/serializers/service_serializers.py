from rest_framework import serializers

from ..models.service_models import Service, Specialty, ServiceCategory


class SpecialtySerializer(serializers.ModelSerializer):
    """
    Specialty serializer.

    Arguments:
        serializers {ModelSerializer} -- ModelSerializer class.
    """
    class Meta:
        model = Specialty

        fields = [
            'id',
            'name'
        ]


class ServiceCategorySerializer(serializers.ModelSerializer):
    """
    Service category serializer.

    Arguments:
        serializers {ModelSerializer} -- ModelSerializer class.
    """
    class Meta:
        model = ServiceCategory

        fields = [
            'id',
            'name'
        ]


class ServiceSerializer(serializers.ModelSerializer):
    """
    Service serializer.

    Arguments:
        serializers {ModelSerializer} -- ModelSerializer class.
    """
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
