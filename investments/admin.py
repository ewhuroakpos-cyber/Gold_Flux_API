from django.contrib import admin
from .models import GoldPrice, Transaction, DepositRequest, WithdrawalRequest, GoldLock

admin.site.register(GoldPrice)
admin.site.register(Transaction)
admin.site.register(DepositRequest)
admin.site.register(WithdrawalRequest)
admin.site.register(GoldLock)
