from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import Document
from app.notification_service import notification_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_notification(doc, reminder_type, days_remaining):
    """
    Send notification to user about expiring document
    
    Supports: Email, SMS, Console logging
    Respects user's reminder interval preferences
    """
    
    # Get user to check preferences
    from app.models.user import User
    db = SessionLocal()
    user = db.query(User).filter(User.id == doc.user_id).first()
    
    # Check if user has this reminder interval enabled
    if user and user.reminder_intervals:
        if not user.reminder_intervals.get(reminder_type, True):
            logger.info(f"⏭️  Skipping {reminder_type} reminder for {doc.document_name} - interval disabled by user")
            db.close()
            return
    
    # Use alternate email if set, otherwise use document email
    email_to_use = doc.email
    if user and user.alternate_email:
        email_to_use = user.alternate_email
        logger.info(f"📧 Using alternate email: {email_to_use}")
    
    db.close()
    
    # Emoji based on urgency
    emoji_map = {
        "6_months": "📅",
        "3_months": "⏰",
        "1_month": "⚠️",
        "7_days": "🚨"
    }
    
    emoji = emoji_map.get(reminder_type, "📄")
    
    # Always log to console
    logger.info(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║  {emoji} REMINDER: Document Expiring Soon                    
    ╠══════════════════════════════════════════════════════════╣
    ║  Document: {doc.document_name}
    ║  Type: {doc.document_type}
    ║  Expiry Date: {doc.expiry_date}
    ║  Days Remaining: {days_remaining}
    ║  Reminder Type: {reminder_type}
    ║  User ID: {doc.user_id}
    ║  Email To: {email_to_use}
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Send Email notification
    if doc.notify_email == "Y":
        success = notification_service.send_email(
            to_email=email_to_use,
            document_name=doc.document_name,
            document_type=doc.document_type,
            expiry_date=str(doc.expiry_date),
            days_remaining=days_remaining,
            reminder_type=reminder_type
        )
        if success:
            logger.info(f"✉️  Email notification sent to {email_to_use}")
        else:
            logger.warning(f"⚠️  Failed to send email to {email_to_use}")
    
    # Send SMS notification
    if doc.phone and doc.notify_sms == "Y":
        success = notification_service.send_sms(
            to_phone=doc.phone,
            document_name=doc.document_name,
            document_type=doc.document_type,
            expiry_date=str(doc.expiry_date),
            days_remaining=days_remaining
        )
        if success:
            logger.info(f"📱 SMS notification sent to {doc.phone}")
        else:
            logger.warning(f"⚠️  Failed to send SMS to {doc.phone}")

def check_expiring_documents():
    """
    Check for expiring documents and send reminders
    
    Runs daily at 9:00 AM (configurable)
    Checks 4 reminder intervals: 6 months, 3 months, 1 month, 7 days
    """
    db = SessionLocal()
    try:
        today = datetime.now().date()
        logger.info(f"🔍 Starting document expiry check for {today}")
        
        # Define reminder intervals
        reminder_intervals = [
            (180, "6_months", "6 months"),
            (90, "3_months", "3 months"),
            (30, "1_month", "1 month"),
            (7, "7_days", "7 days"),
        ]
        
        total_reminders_sent = 0
        
        for days, reminder_type, label in reminder_intervals:
            reminder_date = today + timedelta(days=days)
            
            # Find documents expiring on this date
            documents = db.query(Document).filter(
                Document.expiry_date == reminder_date,
                Document.status != 'expired'
            ).all()
            
            logger.info(f"📊 Checking {label} interval: {len(documents)} documents found")
            
            for doc in documents:
                # Check if reminder already sent
                if doc.reminder_sent and doc.reminder_sent.get(reminder_type):
                    logger.info(f"⏭️  Skipping {doc.document_name} - reminder already sent")
                    continue
                
                # Send notification
                send_notification(doc, reminder_type, days)
                
                # Update reminder_sent tracking
                if not doc.reminder_sent:
                    doc.reminder_sent = {}
                doc.reminder_sent[reminder_type] = datetime.now().isoformat()
                
                total_reminders_sent += 1
        
        # Update document statuses for all documents
        logger.info("📝 Updating document statuses...")
        all_documents = db.query(Document).all()
        status_updates = {"expired": 0, "expiring_soon": 0, "expiring_this_month": 0, "valid": 0}
        
        for doc in all_documents:
            days_until_expiry = (doc.expiry_date - today).days
            old_status = doc.status
            
            if days_until_expiry < 0:
                doc.status = "expired"
            elif days_until_expiry <= 7:
                doc.status = "expiring_soon"
            elif days_until_expiry <= 30:
                doc.status = "expiring_this_month"
            else:
                doc.status = "valid"
            
            if old_status != doc.status:
                logger.info(f"📌 Status changed: {doc.document_name} ({old_status} → {doc.status})")
            
            status_updates[doc.status] += 1
        
        db.commit()
        
        # Summary
        logger.info(f"""
        ╔══════════════════════════════════════════════════════════╗
        ║  ✅ Document Expiry Check Completed                      
        ╠══════════════════════════════════════════════════════════╣
        ║  Date: {today}
        ║  Reminders Sent: {total_reminders_sent}
        ║  
        ║  Status Summary:
        ║    • Valid: {status_updates['valid']}
        ║    • Expiring This Month: {status_updates['expiring_this_month']}
        ║    • Expiring Soon: {status_updates['expiring_soon']}
        ║    • Expired: {status_updates['expired']}
        ╚══════════════════════════════════════════════════════════╝
        """)
        
    except Exception as e:
        logger.error(f"❌ Error in scheduler: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()

# Initialize scheduler
scheduler = BackgroundScheduler()

def start_scheduler():
    """Start the background scheduler"""
    # Run daily at 9:00 AM
    scheduler.add_job(
        check_expiring_documents, 
        'cron', 
        hour=9, 
        minute=0,
        id='document_expiry_check',
        replace_existing=True
    )
    scheduler.start()
    logger.info("⏰ Scheduler started - will check documents daily at 9:00 AM")

def stop_scheduler():
    """Stop the scheduler"""
    scheduler.shutdown()
    logger.info("⏹️  Scheduler stopped")
