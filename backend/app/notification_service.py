"""
Notification Service for Document Reminders

Supports:
- Email notifications (Gmail SMTP / SendGrid)
- SMS notifications (Twilio)
- In-app notifications (future)
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class NotificationService:
    """Handle all notification methods"""
    
    def __init__(self):
        self.email_enabled = bool(settings.SMTP_HOST and settings.SMTP_USER)
        self.sms_enabled = bool(settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN)
        
        if self.email_enabled:
            logger.info("✉️  Email notifications enabled")
        else:
            logger.warning("⚠️  Email notifications disabled (no SMTP config)")
            
        if self.sms_enabled:
            logger.info("📱 SMS notifications enabled")
        else:
            logger.warning("⚠️  SMS notifications disabled (no Twilio config)")
    
    def send_email(self, to_email: str, document_name: str, document_type: str, 
                   expiry_date: str, days_remaining: int, reminder_type: str) -> bool:
        """
        Send email notification
        
        Args:
            to_email: Recipient email address
            document_name: Name of the document
            document_type: Type of document (passport, license, etc.)
            expiry_date: Expiry date string
            days_remaining: Days until expiry
            reminder_type: Type of reminder (6_months, 3_months, etc.)
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.email_enabled:
            logger.warning("Email not configured - skipping email notification")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self._get_email_subject(document_name, days_remaining)
            msg['From'] = f"DateKeeper <{settings.SMTP_USER}>"
            msg['To'] = to_email
            
            # Create HTML and plain text versions
            text_content = self._create_text_email(
                document_name, document_type, expiry_date, days_remaining, reminder_type
            )
            html_content = self._create_html_email(
                document_name, document_type, expiry_date, days_remaining, reminder_type
            )
            
            # Attach both versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"✉️  Email sent to {to_email} for {document_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}")
            return False
    
    def send_sms(self, to_phone: str, document_name: str, document_type: str,
                 expiry_date: str, days_remaining: int) -> bool:
        """
        Send SMS notification via Twilio
        
        Args:
            to_phone: Phone number (E.164 format: +1234567890)
            document_name: Name of the document
            document_type: Type of document
            expiry_date: Expiry date string
            days_remaining: Days until expiry
        
        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.sms_enabled:
            logger.warning("SMS not configured - skipping SMS notification")
            return False
        
        try:
            from twilio.rest import Client
            
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Create message
            message_body = self._create_sms_message(
                document_name, document_type, expiry_date, days_remaining
            )
            
            # Send SMS
            message = client.messages.create(
                body=message_body,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=to_phone
            )
            
            logger.info(f"📱 SMS sent to {to_phone} for {document_name} (SID: {message.sid})")
            return True
            
        except ImportError:
            logger.error("❌ Twilio library not installed. Run: pip install twilio")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to send SMS: {e}")
            return False
    
    def _get_email_subject(self, document_name: str, days_remaining: int) -> str:
        """Generate email subject based on urgency"""
        if days_remaining <= 7:
            return f"🚨 URGENT: {document_name} expires in {days_remaining} days!"
        elif days_remaining <= 30:
            return f"⚠️ Reminder: {document_name} expires in {days_remaining} days"
        elif days_remaining <= 90:
            return f"⏰ Reminder: {document_name} expires in {days_remaining} days"
        else:
            return f"📅 Reminder: {document_name} expires in {days_remaining} days"
    
    def _create_text_email(self, document_name: str, document_type: str,
                          expiry_date: str, days_remaining: int, reminder_type: str) -> str:
        """Create plain text email content"""
        urgency_text = self._get_urgency_text(days_remaining)
        
        return f"""
Hello,

{urgency_text}

Document Details:
- Name: {document_name}
- Type: {document_type.replace('_', ' ').title()}
- Expiry Date: {expiry_date}
- Days Remaining: {days_remaining}

Action Required:
Please renew your {document_type.replace('_', ' ')} before it expires.

Best regards,
DateKeeper Team

---
This is an automated reminder from DateKeeper.
Your privacy is protected - we only store expiry dates, not document images.
"""
    
    def _create_html_email(self, document_name: str, document_type: str,
                          expiry_date: str, days_remaining: int, reminder_type: str) -> str:
        """Create HTML email content"""
        urgency_color = self._get_urgency_color(days_remaining)
        urgency_text = self._get_urgency_text(days_remaining)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
        .alert {{ background: {urgency_color}; color: white; padding: 15px; 
                 border-radius: 8px; margin: 20px 0; text-align: center; font-weight: bold; }}
        .details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; 
                      border-bottom: 1px solid #eee; }}
        .label {{ font-weight: bold; color: #666; }}
        .value {{ color: #333; }}
        .button {{ display: inline-block; background: #667eea; color: white; 
                  padding: 12px 30px; text-decoration: none; border-radius: 8px; 
                  margin: 20px 0; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 DateKeeper</h1>
            <p>Document Expiry Notification</p>
        </div>
        <div class="content">
            <div class="alert">
                {urgency_text}
            </div>
            
            <div class="details">
                <h2>Document Details</h2>
                <div class="detail-row">
                    <span class="label">Document Name:</span>
                    <span class="value">{document_name}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Document Type:</span>
                    <span class="value">{document_type.replace('_', ' ').title()}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Expiry Date:</span>
                    <span class="value">{expiry_date}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Days Remaining:</span>
                    <span class="value">{days_remaining} days</span>
                </div>
            </div>
            
            <p><strong>Action Required:</strong></p>
            <p>Please renew your {document_type.replace('_', ' ')} before it expires to avoid any inconvenience.</p>
            
            <center>
                <a href="http://localhost:5173" class="button">View Dashboard</a>
            </center>
            
            <div class="footer">
                <p>🔒 Your privacy is protected</p>
                <p>We only store expiry dates, not document images.</p>
                <p>This is an automated reminder from DateKeeper.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    def _create_sms_message(self, document_name: str, document_type: str,
                           expiry_date: str, days_remaining: int) -> str:
        """Create SMS message (160 characters max for single SMS)"""
        emoji = "🚨" if days_remaining <= 7 else "⏰"
        return f"{emoji} DateKeeper: Your {document_type.replace('_', ' ')} '{document_name}' expires on {expiry_date} ({days_remaining} days). Please renew soon!"
    
    def _get_urgency_text(self, days_remaining: int) -> str:
        """Get urgency message based on days remaining"""
        if days_remaining <= 7:
            return f"🚨 URGENT: Your document expires in {days_remaining} days!"
        elif days_remaining <= 30:
            return f"⚠️ Important: Your document expires in {days_remaining} days"
        elif days_remaining <= 90:
            return f"⏰ Reminder: Your document expires in {days_remaining} days"
        else:
            return f"📅 Advance Notice: Your document expires in {days_remaining} days"
    
    def _get_urgency_color(self, days_remaining: int) -> str:
        """Get color based on urgency"""
        if days_remaining <= 7:
            return "#ef4444"  # Red
        elif days_remaining <= 30:
            return "#f59e0b"  # Orange
        elif days_remaining <= 90:
            return "#eab308"  # Yellow
        else:
            return "#10b981"  # Green

# Singleton instance
notification_service = NotificationService()
