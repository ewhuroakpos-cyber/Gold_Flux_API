from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q
from .models import User, Wallet
from .serializers import UserSerializer, LoginSerializer

# Create your views here.

class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        wallet = Wallet.objects.create(user=user)
        
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        
        return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        
        # Debug information
        print(f"Login attempt for username: {username}")
        
        # Try to authenticate user
        user = authenticate(username=username, password=password)
        
        if user:
            print(f"Authentication successful for user: {user.username}")
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'user': user_serializer.data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        else:
            print(f"Authentication failed for username: {username}")
            
            # Check if user exists
            try:
                existing_user = User.objects.get(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
                print(f"User exists: {existing_user.username} (active: {existing_user.is_active})")
                return Response({
                    'error': 'Invalid password'
                }, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                print(f"No user found with username/email: {username}")
                return Response({
                    'error': 'User not found'
                }, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
