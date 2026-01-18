"""
Razorpay Subscription Routes - Payment Gateway Integration
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import razorpay
import hmac
import hashlib
from app.config import settings
from app.database import get_db
from app.models.user import User
from app.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/api/razorpay", tags=["Razorpay"])

# Initialize Razorpay client
def get_razorpay_client():
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Razorpay credentials not configured"
        )
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

class CreateSubscriptionRequest(BaseModel):
    plan_id: str

class VerifyPaymentRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_subscription_id: str
    razorpay_signature: str

@router.post("/create-subscription")
async def create_subscription(
    request: CreateSubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create Razorpay subscription
    
    - Creates a subscription for the selected plan
    - Returns subscription ID and payment URL
    """
    try:
        razorpay_client = get_razorpay_client()
        
        # Create subscription
        subscription = razorpay_client.subscription.create({
            "plan_id": request.plan_id,
            "customer_notify": 1,
            "quantity": 1,
            "total_count": 12,  # 12 months
            "notes": {
                "user_id": current_user.id,
                "email": current_user.email
            }
        })
        
        return {
            "subscription_id": subscription['id'],
            "status": subscription['status'],
            "short_url": subscription.get('short_url')
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify-payment")
async def verify_payment(
    request: VerifyPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify Razorpay payment signature
    
    - Verifies payment authenticity
    - Activates user subscription
    - Updates user tier and limits
    """
    try:
        razorpay_client = get_razorpay_client()
        
        # Verify signature
        generated_signature = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            f"{request.razorpay_payment_id}|{request.razorpay_subscription_id}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature != request.razorpay_signature:
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Fetch subscription details
        subscription = razorpay_client.subscription.fetch(request.razorpay_subscription_id)
        
        # Determine tier based on plan_id
        tier = "pro"
        if subscription['plan_id'] == settings.RAZORPAY_PLAN_BUSINESS:
            tier = "business"
        
        # Update user subscription
        current_user.subscription_tier = tier
        current_user.subscription_status = "active"
        current_user.razorpay_subscription_id = request.razorpay_subscription_id
        current_user.document_limit = "-1"  # unlimited
        
        db.commit()
        db.refresh(current_user)
        
        return {
            "success": True,
            "message": "Subscription activated successfully",
            "tier": tier,
            "user": current_user.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Handle Razorpay webhooks
    
    - Listens for subscription events
    - Updates user subscription status
    """
    payload = await request.body()
    signature = request.headers.get('X-Razorpay-Signature')
    
    # Verify webhook signature
    try:
        razorpay_client = get_razorpay_client()
        razorpay_client.utility.verify_webhook_signature(
            payload.decode(),
            signature,
            settings.RAZORPAY_WEBHOOK_SECRET
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Parse event
    import json
    event = json.loads(payload)
    
    event_type = event.get('event')
    
    if event_type == 'subscription.activated':
        # Subscription activated
        subscription = event['payload']['subscription']['entity']
        user_id = subscription['notes'].get('user_id')
        
        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.subscription_status = "active"
                db.commit()
    
    elif event_type == 'subscription.cancelled':
        # Subscription cancelled
        subscription = event['payload']['subscription']['entity']
        
        # Find user by subscription_id
        user = db.query(User).filter(
            User.razorpay_subscription_id == subscription['id']
        ).first()
        
        if user:
            user.subscription_tier = "free"
            user.subscription_status = "cancelled"
            user.document_limit = "10"
            db.commit()
    
    elif event_type == 'subscription.charged':
        # Payment successful
        payment = event['payload']['payment']['entity']
        # Log payment or send receipt
        pass
    
    return {"status": "success"}

@router.get("/current")
async def get_current_subscription(
    current_user: User = Depends(get_current_user)
):
    """
    Get user's current subscription
    
    Returns subscription tier, status, and limits
    """
    return {
        "tier": current_user.subscription_tier or "free",
        "status": current_user.subscription_status or "active",
        "document_limit": current_user.document_limit or "10",
        "razorpay_subscription_id": current_user.razorpay_subscription_id
    }

@router.post("/cancel")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel subscription
    
    - Cancels subscription at end of billing period
    - User retains access until period ends
    """
    try:
        if not current_user.razorpay_subscription_id:
            raise HTTPException(status_code=400, detail="No active subscription")
        
        razorpay_client = get_razorpay_client()
        
        # Cancel in Razorpay
        razorpay_client.subscription.cancel(
            current_user.razorpay_subscription_id,
            cancel_at_cycle_end=1  # Cancel at end of billing period
        )
        
        # Update user
        current_user.subscription_status = "cancelled"
        db.commit()
        
        return {"message": "Subscription will be cancelled at the end of billing period"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
