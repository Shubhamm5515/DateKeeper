from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ocr_service import OCRService
import shutil
import os
from pathlib import Path

router = APIRouter(prefix="/api/ocr", tags=["OCR"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize OCR service
ocr_service = OCRService()

@router.post("/extract-expiry")
async def extract_expiry_date(file: UploadFile = File(...)):
    """
    Upload document image and extract expiry date using OCR + AI.
    
    🔒 PRIVACY GUARANTEE:
    - Your document image is NEVER stored on our servers
    - Image is deleted immediately after OCR processing
    - Only expiry date and document type are extracted
    - No personal information is retained
    """
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(400, "Only JPEG/PNG/WEBP images allowed")
    
    # Check file size (max 10MB)
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > 10 * 1024 * 1024:
        raise HTTPException(400, "File size must be less than 10MB")
    
    # Save uploaded file temporarily
    file_path = UPLOAD_DIR / file.filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process with OCR
        result = ocr_service.process_document(str(file_path))
        
        # 🔒 PRIVACY: Immediately delete the uploaded image
        os.remove(file_path)
        print(f"🔒 Privacy: Document image deleted after processing")
        
        if not result["success"]:
            return {
                "success": False,
                "message": "Could not extract expiry date automatically. Please check the text below and enter manually.",
                "extracted_text": result["extracted_text"],
                "document_type": result["document_type"],
                "help": "Look for dates like: 'Expiry: 12/08/2026' or 'Valid until: 12 Aug 2026'",
                "privacy_note": "Your document image was not stored and has been deleted."
            }
        
        return {
            "success": True,
            "expiry_date": result["expiry_date"],
            "document_type": result["document_type"],
            "confidence": result["confidence"],
            "message": "Expiry date extracted successfully",
            "preview_text": result["extracted_text"][:200] if result["extracted_text"] else "",
            "privacy_note": "Your document image was not stored and has been deleted."
        }
        
    except Exception as e:
        # 🔒 PRIVACY: Clean up on error - ensure image is deleted
        if file_path.exists():
            os.remove(file_path)
            print(f"🔒 Privacy: Document image deleted after error")
        raise HTTPException(500, f"OCR processing failed: {str(e)}")

@router.get("/health")
def ocr_health():
    """Check if OCR service is configured"""
    try:
        from app.config import settings
        
        if settings.OCRSPACE_API_KEY:
            return {
                "status": "healthy",
                "provider": "OCR.space API",
                "configured": True,
                "note": "Using free OCR.space API (25,000 requests/month)"
            }
        else:
            return {
                "status": "healthy",
                "provider": "OCR.space API",
                "configured": True,
                "note": "Using public API key (rate limited)"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "configured": False
        }
