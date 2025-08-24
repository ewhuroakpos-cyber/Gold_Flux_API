from django.urls import path
from .views import (
    TransactionListCreateView, GoldPriceListCreateView,
    AdminUserListView, AdminTransactionListView,
    UserDepositListCreateView, UserWithdrawalListCreateView, UserGoldLockListCreateView,
    AdminDepositListView, AdminWithdrawalListView, AdminGoldLockListView,
    AdminDepositApproveView, AdminWithdrawalApproveView, AdminGoldLockApproveView,
    PortfolioSnapshotView, PriceAlertView, MarketNewsView
)

urlpatterns = [
    # User endpoints
    path('user/transactions/', TransactionListCreateView.as_view(), name='user-transactions'),
    path('user/deposits/', UserDepositListCreateView.as_view(), name='user-deposits'),
    path('user/withdrawals/', UserWithdrawalListCreateView.as_view(), name='user-withdrawals'),
    path('user/gold-locks/', UserGoldLockListCreateView.as_view(), name='user-gold-locks'),
    path('user/portfolio/', PortfolioSnapshotView.as_view(), name='user-portfolio'),
    path('user/price-alerts/', PriceAlertView.as_view(), name='user-price-alerts'),
    path('user/price-alerts/<int:pk>/', PriceAlertView.as_view(), name='user-price-alert-detail'),
    
    # Admin endpoints
    path('admin/users/', AdminUserListView.as_view(), name='admin-users'),
    path('admin/transactions/', AdminTransactionListView.as_view(), name='admin-transactions'),
    path('admin/deposits/', AdminDepositListView.as_view(), name='admin-deposits'),
    path('admin/withdrawals/', AdminWithdrawalListView.as_view(), name='admin-withdrawals'),
    path('admin/gold-locks/', AdminGoldLockListView.as_view(), name='admin-gold-locks'),
    
    # Approval endpoints
    path('admin/deposits/<int:pk>/approve/', AdminDepositApproveView.as_view(), name='admin-deposit-approve'),
    path('admin/withdrawals/<int:pk>/approve/', AdminWithdrawalApproveView.as_view(), name='admin-withdrawal-approve'),
    path('admin/gold-locks/<int:pk>/approve/', AdminGoldLockApproveView.as_view(), name='admin-gold-lock-approve'),
    
    # Market data endpoints
    path('gold/prices/', GoldPriceListCreateView.as_view(), name='gold-prices'),
    path('market/news/', MarketNewsView.as_view(), name='market-news'),
] 