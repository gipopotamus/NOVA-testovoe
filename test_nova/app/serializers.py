from rest_framework import serializers


class FileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    data = serializers.CharField()
