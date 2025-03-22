from rest_framework import serializers
from OcppApp.models import Charger, Transaction

class ChargerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charger
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
