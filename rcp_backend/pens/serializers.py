from rest_framework import serializers
from .models import Pen, Refill

class PenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pen
        fields = '__all__'

class RefillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refill
        fields = '__all__'
