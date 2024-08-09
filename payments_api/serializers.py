from rest_framework import serializers
from .models import Balance, Transaction


class BalanceSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = Balance
        fields = ['amount']


class TransactionSerializer(serializers.ModelSerializer):
    receiver_id = serializers.IntegerField(source='receiver.id', required=True)
    amount = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        model = Transaction
        fields = ['receiver_id', 'amount']
