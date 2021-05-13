from rest_framework import serializers

from bn_app.serializers.beautier_serializers import BeautierProfileSerializer
from bn_app.serializers.service_serializers import ServiceSerializer

from ..models.work_order_models import LineItem, WorkOrder


class LineItemSerializer(serializers.ModelSerializer):
    """
    Line item serializer.

    Arguments:
        serializers {BaseLineItemSerializer} -- BaseLineItemSerializer class.
    """

    class Meta:
        model = LineItem

        fields = [
            'id',
            'service',
            'service_date',
            'service_time',
            'quantity',
            'price',
            'status',
            'beautier_profile',
        ]


class WorkOrderSerializer(serializers.ModelSerializer):
    """
    Work order serializer.

    Arguments:
        serializers {ModelSerializer} -- ModelSerializer class.
    """
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
        ]

    def create(self, validated_data):

        line_items_data = validated_data.pop('line_items')
        work_order = WorkOrder.objects.create(**validated_data)

        for line_item in line_items_data:
            LineItem.objects.create(work_order=work_order, **line_item)

        return work_order
