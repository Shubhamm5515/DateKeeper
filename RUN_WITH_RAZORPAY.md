# 🚀 Run Application with Razorpay

## ⚡ Quick Start Commands

### 1. Setup Razorpay (First Time Only)

**Get Test Keys:**
1. Sign up: https://dashboard.razorpay.com/signup
2. Get keys: https://dashboard.razorpay.com/app/keys
3. Create plans: https://dashboard.razorpay.com/app/subscriptions/plans

**Update .env files with your keys**

### 2. Install Dependencies

```bash
# Backend
cd document-reminder-system/backend
pip install razorpay

# Frontend (no install needed - CDN)
```

### 3. Run Database Migration

```bash
cd document-reminder-system/backend
python migrate_add_subscription.py
```

Expected output:
```
🔄 Starting database migration...
✅ Added subscription_tier column
✅ Added subscription_status column
✅ Added razorpay_subscription_id column
✅ Added document_limit column
✅ Migration completed successfully!
```

### 4. Start Backend Server

```bash
cd document-reminder-system/backend
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ Application started successfully
📊 Environment: development
🔗 Frontend URL: http://localhost:5173
✉️  Email notifications: ENABLED (your-email@gmail.com)
```

### 5. Start Frontend Server (New Terminal)

```bash
cd document-reminder-system/frontend
npm run dev
```

Expected output:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### 6. Test the Application

**Open Browser:**
```
http://localhost:5173
```

**Test Flow:**
1. Click "Pricing" in navigation
2. Click "Upgrade to Pro"
3. Login/Register if needed
4. Razorpay checkout opens
5. Use test card: `4111 1111 1111 1111`
6. Complete payment
7. ✅ Subscription activated!

---

## 🧪 Test Cards

### Credit/Debit Cards

**Success:**
```
Card Number: 4111 1111 1111 1111
Expiry: 12/25
CVV: 123
Name: Test User
```

**Decline:**
```
Card Number: 4111 1111 1111 1234
```

**3D Secure:**
```
Card Number: 5104 0600 0000 0008
```

### UPI

```
UPI ID: success@razorpay
```

### Net Banking

```
Select any bank
Use test credentials
```

---

## 📝 Environment Variables Checklist

### Backend (.env)

```env
# Required for Razorpay
✅ RAZORPAY_KEY_ID="rzp_test_xxxxxxxxxx"
✅ RAZORPAY_KEY_SECRET="xxxxxxxxxxxxxx"
✅ RAZORPAY_PLAN_PRO="plan_xxxxxxxxxxxxx"
✅ RAZORPAY_PLAN_BUSINESS="plan_xxxxxxxxxxxxx"

# Optional for webhooks
⏳ RAZORPAY_WEBHOOK_SECRET="whsec_xxxxxxxxxxxxx"
```

### Frontend (.env)

```env
# Required for Razorpay
✅ VITE_RAZORPAY_KEY_ID="rzp_test_xxxxxxxxxx"
✅ VITE_RAZORPAY_PLAN_PRO="plan_xxxxxxxxxxxxx"
✅ VITE_RAZORPAY_PLAN_BUSINESS="plan_xxxxxxxxxxxxx"
```

---

## 🔍 Verify Installation

### Check Backend

```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "environment": "development"
}
```

### Check Razorpay Endpoint

```bash
# Get current subscription (requires auth token)
curl http://localhost:8000/api/razorpay/current \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Check Frontend

Open: http://localhost:5173/pricing

Should see:
- 4 pricing cards (Free, Pro, Business, Enterprise)
- Payment methods (Cards, UPI, Net Banking, Wallets)
- Upgrade buttons

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error:** `ModuleNotFoundError: No module named 'razorpay'`

**Fix:**
```bash
pip install razorpay
```

### Migration Fails

**Error:** `sqlite3.OperationalError: duplicate column name`

**Fix:** Columns already exist, safe to ignore

### Razorpay Checkout Not Opening

**Check:**
1. ✅ Razorpay script in `index.html`
2. ✅ `VITE_RAZORPAY_KEY_ID` in frontend `.env`
3. ✅ Browser console for errors

**Fix:**
```bash
# Restart frontend
cd frontend
npm run dev
```

### Payment Verification Fails

**Check:**
1. ✅ `RAZORPAY_KEY_SECRET` in backend `.env`
2. ✅ Backend logs for errors

**Fix:** Verify keys match in Razorpay dashboard

---

## 📊 Test Scenarios

### Scenario 1: Free User Upgrades to Pro

1. Register new user
2. Go to `/pricing`
3. Click "Upgrade to Pro"
4. Complete payment with test card
5. ✅ User tier changes to "pro"
6. ✅ Document limit changes to "-1" (unlimited)

### Scenario 2: Pro User Views Current Plan

1. Login as Pro user
2. Go to `/pricing`
3. ✅ "Current Plan" badge shows "pro"
4. ✅ Pro card shows "Current Plan" button (disabled)

### Scenario 3: Check Subscription Status

1. Login as any user
2. Open browser console
3. Run:
```javascript
fetch('http://localhost:8000/api/razorpay/current', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('token')
  }
}).then(r => r.json()).then(console.log)
```
4. ✅ See subscription details

---

## 🎯 Success Indicators

### Backend
- ✅ Server starts without errors
- ✅ Migration completes successfully
- ✅ `/health` endpoint returns 200
- ✅ Razorpay endpoints accessible

### Frontend
- ✅ App loads at http://localhost:5173
- ✅ Pricing page displays correctly
- ✅ Razorpay checkout opens
- ✅ Payment completes successfully

### Database
- ✅ Users table has subscription columns
- ✅ New users have default "free" tier
- ✅ Upgraded users show correct tier

---

## 📞 Support

### Razorpay Issues
- Dashboard: https://dashboard.razorpay.com
- Docs: https://razorpay.com/docs
- Support: support@razorpay.com

### Application Issues
- Check logs in terminal
- Verify .env files
- Check browser console
- Review `RAZORPAY_SETUP_COMPLETE.md`

---

## 🎉 You're Ready!

**Backend**: http://localhost:8000
**Frontend**: http://localhost:5173
**Pricing**: http://localhost:5173/pricing

**Test Card**: `4111 1111 1111 1111`

**Happy Testing!** 💰

---

**Last Updated**: January 18, 2026
