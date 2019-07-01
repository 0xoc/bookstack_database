from rest_framework import serializers

class InsertSerializer(serializers.Serializer):
    json_file = serializers.FileField()

