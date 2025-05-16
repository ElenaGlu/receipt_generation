from rest_framework import serializers


class CreateReceiptSerializer(serializers.Serializer):
    title = serializers.CharField()
    restaurant = serializers.CharField()


class GetReceiptSerializer(serializers.Serializer):
    printer_id = serializers.IntegerField(required=True)
