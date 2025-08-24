from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    gold_holdings = models.DecimalField(max_digits=15, decimal_places=4, default=0.0000)
    
    def __str__(self):
        return f"{self.user.username}'s Wallet"
