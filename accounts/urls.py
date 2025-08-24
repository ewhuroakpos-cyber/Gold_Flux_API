from django.urls import path
from .views import SignupView, LoginView, UserProfileView

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
] 