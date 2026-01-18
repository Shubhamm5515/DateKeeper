import io
import re
from datetime import datetime
from dateutil import parser
import os
import requests
from app.config import settings

class OCRService:
    
    def __init__(self):
        """Initialize OCR service with OCR.space API and optional Gemini"""
        self.api_key = settings.OCRSPACE_API_KEY or 'K87899142388957'  # Free public key
        self.api_url = 'https://api.ocr.space/parse/image'
        self.gemini_key = settings.GEMINI_API_KEY
        print(f"Using OCR.space API for text extraction")
        if self.gemini_key:
            print(f"✨ Gemini AI enabled for intelligent date extraction")
    
    def extract_document_text(self, image_path):
        """Extract text from document using OCR.space"""
        try:
            with open(image_path, 'rb') as image_file:
                # Prepare request
                payload = {
                    'apikey': self.api_key,
                    'language': 'eng',
                    'isOverlayRequired': False,
                    'detectOrientation': True,
                    'scale': True,
                    'OCREngine': 2,  # Engine 2 is more accurate
                }
                
                files = {
                    'file': image_file
                }
                
                # Make request
                response = requests.post(self.api_url, data=payload, files=files)
                response.raise_for_status()
                
                result = response.json()
                
                # Check for errors
                if result.get('IsErroredOnProcessing'):
                    error_msg = result.get('ErrorMessage', ['Unknown error'])[0]
                    raise Exception(f"OCR.space Error: {error_msg}")
                
                # Extract text
                if result.get('ParsedResults') and len(result['ParsedResults']) > 0:
                    text = result['ParsedResults'][0].get('ParsedText', '')
                    return text
                
                return ""
                
        except requests.exceptions.RequestException as e:
            print(f"OCR.space API Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise Exception(f"Failed to call OCR.space API: {str(e)}")
        except Exception as e:
            print(f"OCR Error: {e}")
            raise
    
    def extract_text_from_image(self, image_path):
        """Extract text using OCR.space (same as extract_document_text)"""
        return self.extract_document_text(image_path)
    
    def extract_expiry_with_gemini(self, text):
        """Use Gemini AI to intelligently extract expiry date"""
        if not self.gemini_key:
            return None
        
        try:
            print(f"\n🤖 Using Gemini AI for intelligent extraction...")
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.gemini_key}"
            
            prompt = f"""You are an expert at extracting information from identity documents.

Given this OCR text from a passport/ID/license, extract ONLY the expiry date.

OCR Text:
{text}

Instructions:
1. Find the expiry date (look for: "expiry", "expires", "valid until", "date of expiry", etc.)
2. Return ONLY the date in YYYY-MM-DD format
3. If you find multiple dates, return the EXPIRY date (not birth date or issue date)
4. If no expiry date found, return "NONE"

Examples:
- If you see "Date of expiry: 31.12.2022" → return "2022-12-31"
- If you see "Valid until: 15/08/2025" → return "2025-08-15"
- If you see "Expires: Aug 20, 2024" → return "2024-08-20"

Return ONLY the date in YYYY-MM-DD format or "NONE". No explanation."""

            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 50
                }
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            if 'candidates' in result and len(result['candidates']) > 0:
                extracted = result['candidates'][0]['content']['parts'][0]['text'].strip()
                print(f"Gemini extracted: {extracted}")
                
                if extracted and extracted != "NONE":
                    # Validate it's a proper date
                    try:
                        parsed = datetime.strptime(extracted, '%Y-%m-%d')
                        print(f"✓ Valid date: {parsed.date()}")
                        return extracted
                    except:
                        print(f"✗ Invalid date format from Gemini")
                        return None
            
            return None
            
        except Exception as e:
            print(f"Gemini extraction failed: {e}")
            return None

    def extract_expiry_date(self, text):
        """Extract expiry date from OCR text with multiple patterns"""
        
        # Try Gemini first if available
        if self.gemini_key:
            gemini_date = self.extract_expiry_with_gemini(text)
            if gemini_date:
                return gemini_date
            print("Gemini couldn't extract, falling back to regex patterns...")
        
        print(f"\n=== Date Extraction Debug ===")
        print(f"Extracted text length: {len(text)} characters")
        print(f"First 200 chars: {text[:200]}")
        
        # Comprehensive date patterns
        patterns = [
            # Explicit expiry mentions with various formats
            (r'expir[ye].*?date.*?[:\s]*(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4})', 'Expiry date with slash/dot/dash'),
            (r'expir[ye].*?[:\s]*(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4})', 'Expiry with slash/dot/dash'),
            (r'exp.*?date.*?[:\s]*(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4})', 'Exp date'),
            (r'valid.*?until.*?[:\s]*(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4})', 'Valid until'),
            (r'valid.*?thru.*?[:\s]*(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4})', 'Valid thru'),
            (r'date.*?of.*?expiry.*?[:\s]*(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4})', 'Date of expiry'),
            
            # Date formats with month names
            (r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})', 'DD Mon YYYY'),
            (r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})', 'Mon DD, YYYY'),
            
            # Numeric date formats
            (r'(\d{1,2}[/.\-]\d{1,2}[/.\-]\d{4})', 'DD/MM/YYYY or MM/DD/YYYY'),
            (r'(\d{4}[/.\-]\d{1,2}[/.\-]\d{1,2})', 'YYYY-MM-DD'),
            (r'(\d{2}\s+\d{2}\s+\d{4})', 'DD MM YYYY with spaces'),
            
            # Compact formats
            (r'(\d{8})', 'DDMMYYYY or YYYYMMDD'),
        ]
        
        dates_found = []
        
        for pattern, description in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    date_str = match.group(1) if match.lastindex else match.group(0)
                    print(f"Found potential date: '{date_str}' using pattern: {description}")
                    
                    # Try to parse date
                    parsed_date = None
                    
                    # Handle compact format (8 digits)
                    if len(date_str) == 8 and date_str.isdigit():
                        # Try DDMMYYYY
                        try:
                            parsed_date = datetime.strptime(date_str, '%d%m%Y')
                        except:
                            pass
                        # Try YYYYMMDD
                        if not parsed_date:
                            try:
                                parsed_date = datetime.strptime(date_str, '%Y%m%d')
                            except:
                                pass
                    else:
                        # Use dateutil parser for other formats
                        parsed_date = parser.parse(date_str, fuzzy=True, dayfirst=True)
                    
                    if parsed_date:
                        # Accept dates from 5 years ago to 10 years in future
                        # This allows tracking expired documents too
                        today = datetime.now().date()
                        date_diff = (parsed_date.date() - today).days
                        
                        # Accept dates from 5 years ago to 10 years in future
                        if -1825 <= date_diff <= 3650:  # 5 years ago to 10 years future
                            print(f"  ✓ Parsed as: {parsed_date.date()} (in {date_diff} days)")
                            dates_found.append((parsed_date, date_diff))
                        else:
                            print(f"  ✗ Date out of range: {parsed_date.date()} (too old or too far in future)")
                except Exception as e:
                    print(f"  ✗ Failed to parse: {e}")
                    continue
        
        print(f"\nTotal dates found: {len(dates_found)}")
        
        if dates_found:
            # Sort by date (most recent first)
            # For expired docs, we want the most recent expiry
            # For valid docs, we want the nearest future expiry
            dates_found.sort(key=lambda x: x[0], reverse=True)
            
            # Prefer dates that are in the future or recently expired
            future_dates = [d for d in dates_found if d[1] >= 0]
            recent_past = [d for d in dates_found if -730 <= d[1] < 0]  # Last 2 years
            
            if future_dates:
                best_date = future_dates[-1][0]  # Earliest future date
                print(f"Selected future date: {best_date.date()}")
            elif recent_past:
                best_date = recent_past[0][0]  # Most recent past date
                print(f"Selected recent expiry date: {best_date.date()}")
            else:
                best_date = dates_found[0][0]  # Most recent date overall
                print(f"Selected most recent date: {best_date.date()}")
            
            return best_date.strftime('%Y-%m-%d')
        
        print("No valid dates found")
        return None
    
    def detect_document_type(self, text):
        """Detect document type from text"""
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['passport', 'passeport', 'pasaporte']):
            return 'passport'
        elif any(word in text_lower for word in ['driving', 'driver', 'license', 'licence']):
            return 'driving_license'
        elif any(word in text_lower for word in ['identity', 'national id', 'citizen']):
            return 'national_id'
        elif any(word in text_lower for word in ['visa']):
            return 'visa'
        else:
            return 'other'
    
    def process_document(self, image_path):
        """Complete OCR pipeline with document analysis"""
        
        print(f"\n=== Processing Document ===")
        print(f"Image path: {image_path}")
        
        # Extract text using document-optimized detection
        text = self.extract_document_text(image_path)
        
        print(f"\n=== Full Extracted Text ===")
        print(text)
        print("=" * 50)
        
        # Extract expiry date
        expiry_date = self.extract_expiry_date(text)
        
        # Detect document type
        doc_type = self.detect_document_type(text)
        
        result = {
            "extracted_text": text,
            "expiry_date": expiry_date,
            "document_type": doc_type,
            "success": expiry_date is not None,
            "confidence": "high" if expiry_date else "low"
        }
        
        print(f"\n=== Result ===")
        print(f"Success: {result['success']}")
        print(f"Expiry Date: {expiry_date}")
        print(f"Document Type: {doc_type}")
        print("=" * 50)
        
        return result
