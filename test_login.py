#!/usr/bin/env python3
"""
Test login functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_signup_and_login():
    """Test signup and login flow"""
    print("Testing signup and login...")
    
    # Test data
    test_data = {
        "username": "testuser123",
        "email": "test123@example.com",
        "password": "testpass123"
    }
    
    # Step 1: Signup
    print("1. Testing signup...")
    try:
        signup_response = requests.post(f"{BASE_URL}/auth/signup/", json=test_data)
        print(f"   Signup status: {signup_response.status_code}")
        if signup_response.status_code == 201:
            print("   ✅ Signup successful!")
        else:
            print(f"   ❌ Signup failed: {signup_response.text}")
    except Exception as e:
        print(f"   ❌ Signup error: {e}")
    
    # Step 2: Login with username
    print("\n2. Testing login with username...")
    try:
        login_data = {
            "username": test_data["username"],
            "password": test_data["password"]
        }
        login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"   Login status: {login_response.status_code}")
        if login_response.status_code == 200:
            print("   ✅ Login successful!")
            response_data = login_response.json()
            print(f"   Access token: {response_data.get('access', 'N/A')[:20]}...")
        else:
            print(f"   ❌ Login failed: {login_response.text}")
    except Exception as e:
        print(f"   ❌ Login error: {e}")
    
    # Step 3: Login with email
    print("\n3. Testing login with email...")
    try:
        login_data = {
            "username": test_data["email"],
            "password": test_data["password"]
        }
        login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"   Login status: {login_response.status_code}")
        if login_response.status_code == 200:
            print("   ✅ Login with email successful!")
        else:
            print(f"   ❌ Login with email failed: {login_response.text}")
    except Exception as e:
        print(f"   ❌ Login with email error: {e}")

def test_invalid_login():
    """Test invalid login attempts"""
    print("\n4. Testing invalid login attempts...")
    
    # Test with wrong password
    try:
        login_data = {
            "username": "testuser123",
            "password": "wrongpassword"
        }
        login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"   Wrong password status: {login_response.status_code}")
        if login_response.status_code == 401:
            print("   ✅ Correctly rejected wrong password")
        else:
            print(f"   ❌ Unexpected response: {login_response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test with non-existent user
    try:
        login_data = {
            "username": "nonexistentuser",
            "password": "testpass123"
        }
        login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"   Non-existent user status: {login_response.status_code}")
        if login_response.status_code == 401:
            print("   ✅ Correctly rejected non-existent user")
        else:
            print(f"   ❌ Unexpected response: {login_response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("=== GoldFlux Login Test ===")
    test_signup_and_login()
    test_invalid_login()
    print("\n=== Test Complete ===") 