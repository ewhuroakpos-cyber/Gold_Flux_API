from django.db import models
from accounts.models import User

class GoldPrice(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Gold Price: ${self.price} at {self.timestamp}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Buy Gold'),
        ('SELL', 'Sell Gold'),
    ]
    
    ORDER_TYPES = [
        ('MARKET', 'Market Order'),
        ('LIMIT', 'Limit Order'),
        ('STOP', 'Stop Loss'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    order_type = models.CharField(max_length=6, choices=ORDER_TYPES, default='MARKET')
    amount = models.DecimalField(max_digits=15, decimal_places=4)
    limit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stop_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    executed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    price_at_transaction = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[
        ('PENDING', 'Pending'),
        ('EXECUTED', 'Executed'),
        ('CANCELLED', 'Cancelled'),
    ], default='PENDING')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} {self.get_transaction_type_display()} {self.amount} gold"

class PortfolioSnapshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_snapshots')
    date = models.DateField(auto_now_add=True)
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2)
    gold_value = models.DecimalField(max_digits=15, decimal_places=2)
    gold_holdings = models.DecimalField(max_digits=15, decimal_places=4)
    gold_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} portfolio on {self.date}"

class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='price_alerts')
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    alert_type = models.CharField(max_length=10, choices=[
        ('ABOVE', 'Price Above'),
        ('BELOW', 'Price Below'),
    ])
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    triggered = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.user.username} alert at ${self.target_price}"

class MarketNews(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    source = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    sentiment = models.CharField(max_length=10, choices=[
        ('POSITIVE', 'Positive'),
        ('NEGATIVE', 'Negative'),
        ('NEUTRAL', 'Neutral'),
    ])
    published_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title

class DepositRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    CURRENCY_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('USDT', 'Tether'),
        ('ETH', 'Ethereum'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposit_requests')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=4, choices=CURRENCY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    txid = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_deposits')
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency} ({self.status})"

class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    CURRENCY_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('USDT', 'Tether'),
        ('ETH', 'Ethereum'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal_requests')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=4, choices=CURRENCY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    txid = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_withdrawals')
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency} ({self.status})"

class GoldLock(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('MATURED', 'Matured'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gold_locks')
    amount = models.DecimalField(max_digits=15, decimal_places=4)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    matured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_gold_locks')
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} gold locked ({self.status})"
