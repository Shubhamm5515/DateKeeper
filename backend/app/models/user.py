from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime
import uuid
import json
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Notification preferences
    notify_email = Column(String(1), default="Y")  # Y/N
    notify_sms = Column(String(1), default="N")    # Y/N
    alternate_email = Column(String(255), nullable=True)  # Optional alternate email
    
    # Reminder preferences (stored as JSON string in SQLite)
    _reminder_intervals = Column('reminder_intervals', Text, nullable=True)
    
    # Subscription fields
    subscription_tier = Column(String(20), default="free")  # free, pro, business, enterprise
    subscription_status = Column(String(20), default="active")  # active, cancelled, expired
    razorpay_subscription_id = Column(String(255), nullable=True)
    document_limit = Column(String(10), default="10")  # "10" for free, "-1" for unlimited
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def reminder_intervals(self):
        """Get reminder intervals as dict"""
        if self._reminder_intervals:
            try:
                return json.loads(self._reminder_intervals)
            except:
                pass
        return {
            "6_months": True,
            "3_months": True,
            "1_month": True,
            "7_days": True
        }
    
    @reminder_intervals.setter
    def reminder_intervals(self, value):
        """Set reminder intervals from dict"""
        if value is None:
            self._reminder_intervals = None
        else:
            self._reminder_intervals = json.dumps(value)
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "phone": self.phone,
            "notify_email": self.notify_email,
            "notify_sms": self.notify_sms,
            "alternate_email": self.alternate_email,
            "reminder_intervals": self.reminder_intervals or {
                "6_months": True,
                "3_months": True,
                "1_month": True,
                "7_days": True
            },
            "subscription_tier": self.subscription_tier or "free",
            "subscription_status": self.subscription_status or "active",
            "document_limit": self.document_limit or "10",
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
