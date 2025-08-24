#!/usr/bin/env python3
"""
Simple test script to verify authentication endpoints
Run this after starting the Django server
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_signup():
    """Test user signup"""
    print("Testing signup...")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup/", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 201
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\nTesting login...")
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_profile(access_token):
    """Test user profile endpoint"""
    print("\nTesting profile...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/user/profile/", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing GoldFlux Authentication Endpoints")
    print("=" * 50)
    
    # Test signup
    signup_success = test_signup()
    
    # Test login
    login_success = test_login()
    
    if login_success:
        # Get access token from login response
        login_response = requests.post(f"{BASE_URL}/auth/login/", json={
            "username": "testuser",
            "password": "testpass123"
        })
        if login_response.status_code == 200:
            access_token = login_response.json().get("access")
            if access_token:
                test_profile(access_token)
    
    print("\n" + "=" * 50)
    print("Test completed!") 