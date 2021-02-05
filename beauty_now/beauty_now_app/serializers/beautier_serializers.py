from rest_framework import serializers

from ..serializers.user_serializers import CustomUserSerializer
from ..models.beautier_models import BeautierProfile, BeautierProfileSpecialty, Specialty


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


class BeautierProfilesSpecialtiesSerializer(serializers.ModelSerializer):
    """
    Beautier specialty serializer.

    Arguments:
        serializers {ModelSerializer} -- ModelSerializer class.
    """
    specialty = SpecialtySerializer()

    class Meta:
        model = BeautierProfileSpecialty

        fields = [
            'specialty'
        ]


class BeautierProfileSerializer(serializers.ModelSerializer):
    """
    Beautier serializer.

    Arguments:
        serializers {ModelSerializer} -- ModelSerializer class.
    """
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
