# Document Expiry Reminder - Backend

FastAPI backend with Google Cloud Vision OCR for document expiry date extraction.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your Google Cloud Vision API key to `.env`:
```
GOOGLE_CLOUD_API_KEY=your_api_key_here
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

Server will run on: http://localhost:8000

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### OCR
- `POST /api/ocr/extract-expiry` - Extract expiry date from document image
- `GET /api/ocr/health` - Check OCR service status

### Documents
- `POST /api/documents/` - Create new document
- `GET /api/documents/` - Get all documents
- `GET /api/documents/{id}` - Get specific document
- `PUT /api/documents/{id}` - Update document
- `DELETE /api/documents/{id}` - Delete document
- `GET /api/documents/stats/summary` - Get statistics

## Deployment

### Render
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Add environment variables
5. Deploy

See main README for detailed deployment instructions.
