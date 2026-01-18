"""
Test Email Notification
Quick script to test if Gmail SMTP is configured correctly
"""

from app.config import settings
from app.notification_service import notification_service
from datetime import datetime, timedelta

def test_email():
    """Test email notification"""
    
    print("=" * 60)
    print("📧 EMAIL NOTIFICATION TEST")
    print("=" * 60)
    
    # Check configuration
    print(f"\n📋 Configuration:")
    print(f"   SMTP Host: {settings.SMTP_HOST}")
    print(f"   SMTP Port: {settings.SMTP_PORT}")
    print(f"   SMTP User: {settings.SMTP_USER}")
    print(f"   SMTP Password: {'*' * 16 if settings.SMTP_PASSWORD else 'NOT SET'}")
    
    # Check if enabled
    print(f"\n✅ Email Enabled: {notification_service.email_enabled}")
    
    if not notification_service.email_enabled:
        print("\n❌ Email notifications are NOT enabled!")
        print("\n💡 To enable, add to backend/.env:")
        print("   SMTP_HOST=smtp.gmail.com")
        print("   SMTP_PORT=587")
        print("   SMTP_USER=your-email@gmail.com")
        print("   SMTP_PASSWORD=your-app-password")
        return
    
    # Get test email
    test_email = input(f"\n📧 Enter email to send test to (or press Enter for {settings.SMTP_USER}): ").strip()
    if not test_email:
        test_email = settings.SMTP_USER
    
    print(f"\n📤 Sending test email to: {test_email}")
    print("⏳ Please wait...")
    
    # Send test email
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
            print("💡 Don't forget to check spam folder if you don't see it")
        else:
            print("\n❌ FAILED! Email was not sent")
            print("💡 Check the error messages above")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n💡 Common issues:")
        print("   1. Wrong app password (must be 16 characters, no spaces)")
        print("   2. 2-Step Verification not enabled")
        print("   3. Firewall blocking SMTP port 587")
        print("   4. Wrong SMTP host/port")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_email()
