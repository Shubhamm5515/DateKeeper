@echo off
echo Starting DateKeeper Backend on port 8001...
echo.
echo Backend will be available at: http://localhost:8001
echo API Documentation: http://localhost:8001/docs
echo.
python -m uvicorn app.main:app --reload --port 8001
