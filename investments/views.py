from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
from .models import GoldPrice, Transaction, DepositRequest, WithdrawalRequest, GoldLock, PortfolioSnapshot, PriceAlert, MarketNews
from .serializers import (
    GoldPriceSerializer, TransactionSerializer, DepositRequestSerializer,
    WithdrawalRequestSerializer, GoldLockSerializer, PortfolioSnapshotSerializer,
    PriceAlertSerializer, MarketNewsSerializer
)
from accounts.models import User
from accounts.serializers import UserSerializer

class IsAdminOrReadOnly:
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated and request.user.is_admin

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        transaction_type = request.data.get('transaction_type')
        amount = request.data.get('amount')
        order_type = request.data.get('order_type', 'MARKET')
        limit_price = request.data.get('limit_price')
        stop_price = request.data.get('stop_price')
        
        # Get current gold price
        try:
            current_price = GoldPrice.objects.latest('timestamp').price
        except GoldPrice.DoesNotExist:
            return Response({'error': 'No gold price available'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        wallet = user.wallet
        
        # For market orders, execute immediately
        if order_type == 'MARKET':
            if transaction_type == 'BUY':
                cost = float(amount) * float(current_price)
                if wallet.balance < cost:
                    return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
                
                wallet.balance -= cost
                wallet.gold_holdings += float(amount)
                
            elif transaction_type == 'SELL':
                if wallet.gold_holdings < float(amount):
                    return Response({'error': 'Insufficient gold holdings'}, status=status.HTTP_400_BAD_REQUEST)
                
                wallet.gold_holdings -= float(amount)
                wallet.balance += float(amount) * float(current_price)
            
            wallet.save()
            
            transaction = Transaction.objects.create(
                user=user,
                transaction_type=transaction_type,
                order_type=order_type,
                amount=amount,
                price_at_transaction=current_price,
                executed_price=current_price,
                status='EXECUTED'
            )
        else:
            # For limit/stop orders, create pending order
            transaction = Transaction.objects.create(
                user=user,
                transaction_type=transaction_type,
                order_type=order_type,
                amount=amount,
                price_at_transaction=current_price,
                limit_price=limit_price,
                stop_price=stop_price,
                status='PENDING'
            )
        
        serializer = self.get_serializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PortfolioSnapshotView(generics.ListCreateAPIView):
    serializer_class = PortfolioSnapshotSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PortfolioSnapshot.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        wallet = user.wallet
        
        # Get current gold price
        try:
            current_price = GoldPrice.objects.latest('timestamp').price
        except GoldPrice.DoesNotExist:
            return Response({'error': 'No gold price available'}, status=status.HTTP_400_BAD_REQUEST)
        
        gold_value = float(wallet.gold_holdings) * float(current_price)
        total_value = float(wallet.balance) + gold_value
        
        snapshot = PortfolioSnapshot.objects.create(
            user=user,
            total_value=total_value,
            cash_balance=wallet.balance,
            gold_value=gold_value,
            gold_holdings=wallet.gold_holdings,
            gold_price=current_price
        )
        
        serializer = self.get_serializer(snapshot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PriceAlertView(generics.ListCreateAPIView):
    serializer_class = PriceAlertSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user, is_active=True)
    
    def destroy(self, request, *args, **kwargs):
        alert = self.get_object()
        alert.is_active = False
        alert.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MarketNewsView(generics.ListAPIView):
    serializer_class = MarketNewsSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return MarketNews.objects.all()[:10]  # Return latest 10 news items

class GoldPriceListCreateView(generics.ListCreateAPIView):
    serializer_class = GoldPriceSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        return GoldPrice.objects.all()

class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            return User.objects.none()
        return User.objects.all()

class AdminTransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            return Transaction.objects.none()
        return Transaction.objects.all()

# User deposit/withdrawal/gold lock views
class UserDepositListCreateView(generics.ListCreateAPIView):
    serializer_class = DepositRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DepositRequest.objects.filter(user=self.request.user)

class UserWithdrawalListCreateView(generics.ListCreateAPIView):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WithdrawalRequest.objects.filter(user=self.request.user)

class UserGoldLockListCreateView(generics.ListCreateAPIView):
    serializer_class = GoldLockSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return GoldLock.objects.filter(user=self.request.user)

# Admin management views
class AdminDepositListView(generics.ListAPIView):
    serializer_class = DepositRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            return DepositRequest.objects.none()
        return DepositRequest.objects.all()

class AdminWithdrawalListView(generics.ListAPIView):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            return WithdrawalRequest.objects.none()
        return WithdrawalRequest.objects.all()

class AdminGoldLockListView(generics.ListAPIView):
    serializer_class = GoldLockSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            return GoldLock.objects.none()
        return GoldLock.objects.all()

# Approval views
class AdminDepositApproveView(generics.UpdateAPIView):
    serializer_class = DepositRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            return DepositRequest.objects.none()
        return DepositRequest.objects.filter(status='PENDING')
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        deposit = self.get_object()
        action = request.data.get('action')
        
        if action == 'approve':
            deposit.status = 'APPROVED'
            deposit.approved_at = timezone.now()
            deposit.approved_by = request.user
            deposit.save()
            
            # Update user's wallet balance
            user = deposit.user
            wallet = user.wallet
            wallet.balance += deposit.amount
            wallet.save()
            
        elif action == 'reject':
            deposit.status = 'REJECTED'
            deposit.approved_at = timezone.now()
            deposit.approved_by = request.user
            deposit.save()
        
        serializer = self.get_serializer(deposit)
        return Response(serializer.data)

class AdminWithdrawalApproveView(generics.UpdateAPIView):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            return WithdrawalRequest.objects.none()
        return WithdrawalRequest.objects.filter(status='PENDING')
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        withdrawal = self.get_object()
        action = request.data.get('action')
        
        if action == 'approve':
            user = withdrawal.user
            wallet = user.wallet
            
            if wallet.balance < withdrawal.amount:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
            
            withdrawal.status = 'APPROVED'
            withdrawal.approved_at = timezone.now()
            withdrawal.approved_by = request.user
            withdrawal.save()
            
            wallet.balance -= withdrawal.amount
            wallet.save()
            
        elif action == 'reject':
            withdrawal.status = 'REJECTED'
            withdrawal.approved_at = timezone.now()
            withdrawal.approved_by = request.user
            withdrawal.save()
        
        serializer = self.get_serializer(withdrawal)
        return Response(serializer.data)

class AdminGoldLockApproveView(generics.UpdateAPIView):
    serializer_class = GoldLockSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_admin:
            return GoldLock.objects.none()
        return GoldLock.objects.filter(status='PENDING')
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        gold_lock = self.get_object()
        action = request.data.get('action')
        
        if action == 'approve':
            user = gold_lock.user
            wallet = user.wallet
            
            if wallet.gold_holdings < gold_lock.amount:
                return Response({'error': 'Insufficient gold holdings'}, status=status.HTTP_400_BAD_REQUEST)
            
            gold_lock.status = 'APPROVED'
            gold_lock.approved_at = timezone.now()
            gold_lock.approved_by = request.user
            gold_lock.save()
            
            wallet.gold_holdings -= gold_lock.amount
            wallet.save()
            
        elif action == 'reject':
            gold_lock.status = 'REJECTED'
            gold_lock.approved_at = timezone.now()
            gold_lock.approved_by = request.user
            gold_lock.save()
        
        serializer = self.get_serializer(gold_lock)
        return Response(serializer.data)
