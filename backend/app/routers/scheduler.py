from fastapi import APIRouter, HTTPException
from app.scheduler import check_expiring_documents, scheduler
from datetime import datetime

router = APIRouter(prefix="/api/scheduler", tags=["Scheduler"])

@router.get("/health")
def scheduler_health():
    """Check scheduler status and next run time"""
    try:
        is_running = scheduler.running
        jobs = scheduler.get_jobs()
        
        if jobs:
            next_run = jobs[0].next_run_time
            job_id = jobs[0].id
        else:
            next_run = None
            job_id = None
        
        return {
            "status": "running" if is_running else "stopped",
            "scheduler_running": is_running,
            "job_id": job_id,
            "next_run_time": next_run.isoformat() if next_run else None,
            "current_time": datetime.now().isoformat(),
            "schedule": "Daily at 9:00 AM",
            "message": "Scheduler is healthy and running" if is_running else "Scheduler is not running"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.post("/run-now")
def run_scheduler_now():
    """
    Manually trigger the document expiry check immediately
    
    Useful for:
    - Testing the reminder system
    - Debugging notification logic
    - Manual execution without waiting for scheduled time
    """
    try:
        check_expiring_documents()
        return {
            "success": True,
            "message": "Document expiry check executed successfully",
            "executed_at": datetime.now().isoformat(),
            "note": "Check server logs for detailed results"
        }
    except Exception as e:
        raise HTTPException(500, f"Failed to run scheduler: {str(e)}")

@router.get("/info")
def scheduler_info():
    """Get detailed information about the scheduler configuration"""
    return {
        "scheduler_type": "APScheduler (BackgroundScheduler)",
        "schedule": {
            "type": "cron",
            "hour": 9,
            "minute": 0,
            "timezone": "System timezone"
        },
        "reminder_intervals": [
            {"days": 180, "type": "6_months", "label": "6 months before expiry"},
            {"days": 90, "type": "3_months", "label": "3 months before expiry"},
            {"days": 30, "type": "1_month", "label": "1 month before expiry"},
            {"days": 7, "type": "7_days", "label": "7 days before expiry"}
        ],
        "status_thresholds": {
            "expired": "< 0 days",
            "expiring_soon": "≤ 7 days",
            "expiring_this_month": "≤ 30 days",
            "valid": "> 30 days"
        },
        "features": [
            "Automatic daily checks",
            "Duplicate reminder prevention",
            "Status auto-updates",
            "Console logging",
            "Error handling"
        ],
        "notification_methods": {
            "implemented": ["Console logging"],
            "planned": ["Email", "SMS", "Push notifications", "In-app alerts"]
        }
    }
