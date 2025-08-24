from rest_framework import serializers
from .models import GoldPrice, Transaction, DepositRequest, WithdrawalRequest, GoldLock, PortfolioSnapshot, PriceAlert, MarketNews

class GoldPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldPrice
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Transaction
        fields = '__all__'

class PortfolioSnapshotSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = PortfolioSnapshot
        fields = '__all__'

class PriceAlertSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = PriceAlert
        fields = '__all__'

class MarketNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketNews
        fields = '__all__'

class DepositRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    approved_by = serializers.CharField(source='approved_by.username', read_only=True)
    
    class Meta:
        model = DepositRequest
        fields = '__all__'

class WithdrawalRequestSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    approved_by = serializers.CharField(source='approved_by.username', read_only=True)
    
    class Meta:
        model = WithdrawalRequest
        fields = '__all__'

class GoldLockSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    approved_by = serializers.CharField(source='approved_by.username', read_only=True)
    
    class Meta:
        model = GoldLock
        fields = '__all__' 