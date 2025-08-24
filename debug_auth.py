#!/usr/bin/env python3
"""
Debug authentication issues
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gold_flux.settings')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import User

def test_user_creation():
    """Test creating a user and authenticating"""
    print("Testing user creation and authentication...")
    
    # Create a test user
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
    
    # Check if user exists
    try:
        user = User.objects.get(username=username)
        print(f"User {username} already exists")
    except User.DoesNotExist:
        print(f"Creating user {username}...")
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"User {username} created successfully")
    
    # Test authentication
    print(f"Testing authentication for {username}...")
    authenticated_user = authenticate(username=username, password=password)
    
    if authenticated_user:
        print("✅ Authentication successful!")
        print(f"User ID: {authenticated_user.id}")
        print(f"Username: {authenticated_user.username}")
        print(f"Email: {authenticated_user.email}")
        print(f"Is active: {authenticated_user.is_active}")
        print(f"Is staff: {authenticated_user.is_staff}")
        print(f"Is admin: {authenticated_user.is_admin}")
    else:
        print("❌ Authentication failed!")
        
        # Check user details
        user = User.objects.get(username=username)
        print(f"User exists in database:")
        print(f"  ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Is active: {user.is_active}")
        print(f"  Password set: {user.has_usable_password()}")
        
        # Try different authentication methods
        print("\nTrying different authentication methods...")
        
        # Try with email
        auth_by_email = authenticate(username=email, password=password)
        if auth_by_email:
            print("✅ Authentication with email successful!")
        else:
            print("❌ Authentication with email failed")
        
        # Try case insensitive
        auth_case = authenticate(username=username.upper(), password=password)
        if auth_case:
            print("✅ Authentication with uppercase username successful!")
        else:
            print("❌ Authentication with uppercase username failed")

def test_existing_users():
    """List all existing users"""
    print("\nExisting users in database:")
    users = User.objects.all()
    for user in users:
        print(f"  - {user.username} ({user.email}) - Active: {user.is_active}")

if __name__ == "__main__":
    print("=== GoldFlux Authentication Debug ===")
    test_existing_users()
    test_user_creation()
    print("\n=== Debug Complete ===") 