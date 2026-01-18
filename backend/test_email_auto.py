"""
Automated Email Test - No user input required
"""

from app.config import settings
from app.notification_service import notification_service

def test_email_auto():
    """Test email notification automatically"""
    
    print("=" * 60)
    print("📧 AUTOMATED EMAIL TEST")
    print("=" * 60)
    
    # Check configuration
    print(f"\n📋 Configuration:")
    print(f"   SMTP Host: {settings.SMTP_HOST}")
    print(f"   SMTP Port: {settings.SMTP_PORT}")
    print(f"   SMTP User: {settings.SMTP_USER}")
    print(f"   Email Enabled: {notification_service.email_enabled}")
    
    if not notification_service.email_enabled:
        print("\n❌ Email notifications are NOT enabled!")
        return
    
    # Send test email to configured email
    test_email = settings.SMTP_USER
    print(f"\n📤 Sending test email to: {test_email}")
    print("⏳ Please wait...")
    
    try:
        success = notification_service.send_email(
            to_email=test_email,
            document_name="Test Passport",
            document_type="passport",
            expiry_date="2026-07-15",
            days_remaining=180,
            reminder_type="6_months"
        )
        
        if success:
            print("\n✅ SUCCESS! Email sent successfully!")
            print(f"📬 Check your inbox: {test_email}")
            print("💡 Subject: 📅 Reminder: Test Passport expires in 180 days")
            print("💡 Don't forget to check spam folder!")
        else:
            print("\n❌ FAILED! Email was not sent")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_email_auto()
