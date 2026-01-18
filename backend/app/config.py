from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./documents.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    
    # OCR.space API (Free - no billing required)
    OCRSPACE_API_KEY: Optional[str] = None
    
    # Gemini API (Free - for intelligent date extraction)
    GEMINI_API_KEY: Optional[str] = None
    
    # Google Cloud Vision (Alternative - requires billing)
    GOOGLE_CLOUD_API_KEY: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS_JSON: Optional[str] = None
    
    # Google OAuth (for login)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    # Email Notifications (SMTP - Gmail or custom)
    SMTP_HOST: Optional[str] = None  # e.g., smtp.gmail.com
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None  # Your email
    SMTP_PASSWORD: Optional[str] = None  # App password for Gmail
    
    # Google OAuth (for Sign in with Google)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    # SMS Notifications (Twilio)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None  # Format: +1234567890
    
    # SendGrid (Alternative email service)
    SENDGRID_API_KEY: Optional[str] = None
    SENDGRID_FROM_EMAIL: str = "noreply@example.com"
    
    # Razorpay Payment Gateway
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = None
    RAZORPAY_PLAN_PRO: Optional[str] = None
    RAZORPAY_PLAN_BUSINESS: Optional[str] = None
    
    # CORS
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()
