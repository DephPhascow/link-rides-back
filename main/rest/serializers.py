from rest_framework import serializers
from main.models import TmpModel

class TmpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TmpModel
        fields = ["name", "description", ]