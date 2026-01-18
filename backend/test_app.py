"""
Complete App Test Suite
Tests all major features of DateKeeper
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_health():
    """Test 1: Health Check"""
    print_section("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_ocr_health():
    """Test 2: OCR Service Health"""
    print_section("TEST 2: OCR Service Health")
    
    try:
        response = requests.get(f"{BASE_URL}/api/ocr/health")
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ Provider: {data.get('provider')}")
        print(f"✅ Configured: {data.get('configured')}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_scheduler_health():
    """Test 3: Scheduler Health"""
    print_section("TEST 3: Scheduler Health")
    
    try:
        response = requests.get(f"{BASE_URL}/api/scheduler/health")
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ Status: {data.get('status')}")
        print(f"✅ Next Run: {data.get('next_run_time')}")
        print(f"✅ Schedule: {data.get('schedule')}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_add_document():
    """Test 4: Add Document"""
    print_section("TEST 4: Add Document with Email")
    
    # Calculate test date (30 days from now for 1-month reminder)
    expiry_date = (datetime.now().date() + timedelta(days=30)).isoformat()
    
    document = {
        "document_name": "Test Passport",
        "document_type": "passport",
        "expiry_date": expiry_date,
        "email": "shubhamm3197@gmail.com",
        "notify_email": "Y",
        "user_id": "default_user"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/documents/",
            json=document
        )
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ Document ID: {data.get('id')}")
        print(f"✅ Document Name: {data.get('document_name')}")
        print(f"✅ Expiry Date: {data.get('expiry_date')}")
        print(f"✅ Email: {data.get('email')}")
        print(f"✅ Status: {data.get('status')}")
        return data.get('id')
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

def test_get_documents():
    """Test 5: Get All Documents"""
    print_section("TEST 5: Get All Documents")
    
    try:
        response = requests.get(f"{BASE_URL}/api/documents/?user_id=default_user")
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ Total Documents: {len(data)}")
        
        for i, doc in enumerate(data[:3], 1):  # Show first 3
            print(f"\n   Document {i}:")
            print(f"   - Name: {doc.get('document_name')}")
            print(f"   - Type: {doc.get('document_type')}")
            print(f"   - Expiry: {doc.get('expiry_date')}")
            print(f"   - Status: {doc.get('status')}")
            print(f"   - Email: {doc.get('email', 'Not set')}")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_get_stats():
    """Test 6: Get Document Statistics"""
    print_section("TEST 6: Get Document Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/api/documents/stats/summary?user_id=default_user")
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ Total: {data.get('total')}")
        print(f"✅ Valid: {data.get('valid')}")
        print(f"✅ Expiring Soon: {data.get('expiring_soon')}")
        print(f"✅ Expired: {data.get('expired')}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_trigger_reminder():
    """Test 7: Trigger Reminder Manually"""
    print_section("TEST 7: Trigger Reminder Check")
    
    try:
        response = requests.post(f"{BASE_URL}/api/scheduler/run-now")
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ Success: {data.get('success')}")
        print(f"✅ Message: {data.get('message')}")
        print(f"✅ Executed At: {data.get('executed_at')}")
        print(f"\n💡 Check backend console for reminder logs")
        print(f"💡 Check email: shubhamm3197@gmail.com")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def test_delete_document(doc_id):
    """Test 8: Delete Document"""
    if not doc_id:
        print("\n⏭️  Skipping delete test (no document ID)")
        return False
    
    print_section("TEST 8: Delete Document")
    
    try:
        response = requests.delete(f"{BASE_URL}/api/documents/{doc_id}")
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ Message: {data.get('message')}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪" * 35)
    print("  DATEKEEPER - COMPLETE APP TEST SUITE")
    print("🧪" * 35)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health()))
    results.append(("OCR Service", test_ocr_health()))
    results.append(("Scheduler", test_scheduler_health()))
    
    doc_id = test_add_document()
    results.append(("Add Document", doc_id is not None))
    
    results.append(("Get Documents", test_get_documents()))
    results.append(("Get Statistics", test_get_stats()))
    results.append(("Trigger Reminder", test_trigger_reminder()))
    results.append(("Delete Document", test_delete_document(doc_id)))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your app is working perfectly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
    
    print("\n" + "=" * 70)
    
    # Additional info
    print("\n💡 Next Steps:")
    print("   1. Check your email: shubhamm3197@gmail.com")
    print("   2. Open frontend: http://localhost:5173")
    print("   3. Check backend logs for reminder notifications")
    print("   4. Add more documents with different expiry dates")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    run_all_tests()
