"""
Keep Render backend alive by pinging it every 10 minutes
Run this script on a free service like GitHub Actions or Render Cron Job
"""

import requests
import time
import os

BACKEND_URL = os.getenv('BACKEND_URL', 'https://your-app.onrender.com')

def ping_backend():
    try:
        response = requests.get(f'{BACKEND_URL}/api/scheduler/health', timeout=10)
        if response.status_code == 200:
            print(f'✅ Backend is alive: {response.json()}')
        else:
            print(f'⚠️ Backend responded with status {response.status_code}')
    except Exception as e:
        print(f'❌ Failed to ping backend: {e}')

if __name__ == '__main__':
    while True:
        ping_backend()
        time.sleep(600)  # Wait 10 minutes
