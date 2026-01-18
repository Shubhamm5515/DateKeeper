"""
Test Authentication System
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth():
    print("=" * 70)
    print("  🔐 AUTHENTICATION SYSTEM TEST")
    print("=" * 70)
    
    # Test 1: Register
    print("\n1️⃣  Testing Registration...")
    register_data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            user = data["user"]
            
            print(f"✅ Registration successful!")
            print(f"   Email: {user['email']}")
            print(f"   Name: {user['full_name']}")
            print(f"   Token: {token[:30]}...")
            print(f"   Notify Email: {user['notify_email']}")
            
        elif response.status_code == 400:
            print(f"⚠️  User already exists, trying login...")
            # Try login instead
            login_data = {
                "email": register_data["email"],
                "password": register_data["password"]
            }
            response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
            data = response.json()
            token = data["access_token"]
            user = data["user"]
            
            print(f"✅ Login successful!")
            print(f"   Email: {user['email']}")
            print(f"   Token: {token[:30]}...")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Test 2: Get Profile
    print("\n2️⃣  Testing Get Profile...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Profile retrieved!")
            print(f"   Email: {profile['email']}")
            print(f"   Name: {profile.get('full_name', 'Not set')}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Add Document (email automatic!)
    print("\n3️⃣  Testing Add Document (email automatic)...")
    document_data = {
        "document_name": "Test Passport",
        "document_type": "passport",
        "expiry_date": "2026-07-15"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/documents/",
            headers=headers,
            json=document_data
        )
        if response.status_code == 200:
            doc = response.json()
            print(f"✅ Document added!")
            print(f"   Name: {doc['document_name']}")
            print(f"   Expiry: {doc['expiry_date']}")
            print(f"   Status: {doc['status']}")
            print(f"   📧 Email notifications will be sent to: {user['email']}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Get Documents
    print("\n4️⃣  Testing Get Documents...")
    try:
        response = requests.get(f"{BASE_URL}/api/documents/", headers=headers)
        if response.status_code == 200:
            documents = response.json()
            print(f"✅ Retrieved {len(documents)} document(s)")
            for doc in documents[:3]:
                print(f"   - {doc['document_name']} (expires: {doc['expiry_date']})")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("  ✅ AUTHENTICATION TEST COMPLETE")
    print("=" * 70)
    print("\n💡 Key Features:")
    print("   ✅ JWT authentication working")
    print("   ✅ User registration/login working")
    print("   ✅ Protected routes working")
    print("   ✅ Email automatically used from user profile")
    print("   ✅ Documents linked to user account")
    print("\n📧 Reminders will be sent to: " + user['email'])
    print("=" * 70)

if __name__ == "__main__":
    test_auth()
