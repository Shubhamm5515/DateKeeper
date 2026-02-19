from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import ocr, documents, scheduler, auth, google_auth
from app.scheduler import start_scheduler, stop_scheduler

# Import models to create tables
from app.models import document, user

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Document Expiry Reminder API",
    description="API for managing document expiry reminders with OCR",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # React default
    settings.FRONTEND_URL,
    "https://date-keeper-ivory.vercel.app",  # Production frontend
]

# Remove duplicates
origins = list(set(origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(google_auth.router)
app.include_router(ocr.router)
app.include_router(documents.router)
app.include_router(scheduler.router)

@app.on_event("startup")
def startup_event():
    """Run on application startup"""
    from app.notification_service import notification_service
    
    start_scheduler()
    print("✅ Application started successfully")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    print(f"🔗 Frontend URL: {settings.FRONTEND_URL}")
    
    # Show notification status
    if notification_service.email_enabled:
        print(f"✉️  Email notifications: ENABLED ({settings.SMTP_USER})")
    else:
        print("⚠️  Email notifications: DISABLED (configure SMTP in .env)")
    
    if notification_service.sms_enabled:
        print(f"📱 SMS notifications: ENABLED ({settings.TWILIO_PHONE_NUMBER})")
    else:
        print("⚠️  SMS notifications: DISABLED (configure Twilio in .env)")

@app.on_event("shutdown")
def shutdown_event():
    """Run on application shutdown"""
    stop_scheduler()
    print("👋 Application shutting down")

@app.get("/")
def read_root():
    return {
        "message": "Document Expiry Reminder API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }
