# 📧 Email Setup Guide - SMTP Configuration

## What is SMTP_USER?

**SMTP_USER** is your email address that DateKeeper uses to **send reminder emails** to users.

---

## 🎯 What It's Used For

### Email Notifications Sent by DateKeeper:

1. **Document Expiry Reminders**
   - "Your Passport expires in 7 days"
   - "Your License expires in 30 days"
   - Sent automatically by the scheduler

2. **Email Format**:
   ```
   From: DateKeeper <your-email@gmail.com>  ← SMTP_USER
   To: user@example.com
   Subject: 🚨 Document Expiring Soon - Passport
   ```

3. **When Emails Are Sent**:
   - 180 days before expiry (6 months)
   - 90 days before expiry (3 months)
   - 30 days before expiry (1 month)
   - 7 days before expiry (1 week)

---

## 🔧 How to Set Up Gmail SMTP (FREE)

### Step 1: Enable 2-Step Verification (5 minutes)

1. Go to: https://myaccount.google.com/security
2. Scroll to "How you sign in to Google"
3. Click "2-Step Verification"
4. Click "Get Started"
5. Follow the steps to enable 2FA
6. ✅ Done!

### Step 2: Generate App Password (2 minutes)

1. Go to: https://myaccount.google.com/apppasswords
2. **App name**: Enter `DateKeeper`
3. Click "Create"
4. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)
5. ⚠️ **Save this password** - you can't see it again!

### Step 3: Add to Environment Variables

**For Local Development** (`backend/.env`):
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com          ← Your Gmail address
SMTP_PASSWORD=abcd efgh ijkl mnop       ← App password from Step 2
```

**For Production** (Render Dashboard):
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop          ← Remove spaces
```

---

## 📧 Email Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    DateKeeper App                       │
│                                                         │
│  1. Scheduler runs daily at 9:00 AM                    │
│     ↓                                                   │
│  2. Checks documents expiring in 7/30/90/180 days     │
│     ↓                                                   │
│  3. Sends email via SMTP                               │
│     ↓                                                   │
│  ┌──────────────────────────────────────┐             │
│  │ From: DateKeeper <SMTP_USER>         │             │
│  │ To: user@example.com                 │             │
│  │ Subject: Document Expiring Soon      │             │
│  │                                       │             │
│  │ Your Passport expires in 7 days!     │             │
│  └──────────────────────────────────────┘             │
│     ↓                                                   │
│  4. Gmail SMTP Server (smtp.gmail.com:587)            │
│     ↓                                                   │
│  5. Email delivered to user's inbox                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 Example Email Sent

**From**: DateKeeper <shubhamm3197@gmail.com>  
**To**: user@example.com  
**Subject**: 🚨 Document Expiring Soon - Passport

```
Hi there,

Your Passport is expiring soon!

Document: My Passport
Expiry Date: February 15, 2026
Days Remaining: 7 days

⚠️ URGENT: Please renew your document as soon as possible.

[View Dashboard]

Best regards,
DateKeeper Team

---
This is an automated reminder from DateKeeper.
Your privacy is protected - we only store expiry dates, not document images.
```

---

## ⚙️ Configuration Options

### Option 1: Gmail (Recommended - FREE)
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Limits**:
- ✅ 500 emails/day (enough for 500 users)
- ✅ Free forever
- ✅ Reliable delivery
- ⚠️ Requires 2FA + App Password

### Option 2: SendGrid (Alternative - FREE)
```env
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
```

**Limits**:
- ✅ 100 emails/day (free tier)
- ✅ Better for custom domains
- ✅ Email analytics
- ⚠️ Requires domain verification

### Option 3: Custom SMTP Server
```env
SMTP_HOST=mail.yourdomain.com
SMTP_PORT=587
SMTP_USER=noreply@yourdomain.com
SMTP_PASSWORD=your-password
```

---

## 🧪 Test Email Configuration

### Method 1: Use Test Script

```bash
cd document-reminder-system/backend
python test_email.py
```

Expected output:
```
✅ Email sent successfully!
Check your inbox: your-email@gmail.com
```

### Method 2: Manual Test via Dashboard

1. Deploy your app
2. Register a new account
3. Add a document expiring in 7 days
4. Click "Test Reminders" button
5. Check your email inbox

---

## 🐛 Troubleshooting

### ❌ Error: "Username and Password not accepted"

**Solution**:
1. Enable 2-Step Verification
2. Generate App Password (not your regular Gmail password)
3. Use App Password in `SMTP_PASSWORD`

### ❌ Error: "Connection refused"

**Solution**:
1. Check `SMTP_HOST=smtp.gmail.com` (not mail.google.com)
2. Check `SMTP_PORT=587` (not 465 or 25)
3. Check firewall/network allows port 587

### ❌ Error: "Authentication failed"

**Solution**:
1. Remove spaces from App Password: `abcd efgh ijkl mnop` → `abcdefghijklmnop`
2. Regenerate App Password if needed
3. Check SMTP_USER is correct email

### ❌ Emails going to Spam

**Solution**:
1. Add "DateKeeper" to contacts
2. Mark first email as "Not Spam"
3. Consider using custom domain with SPF/DKIM records

---

## 🔒 Security Best Practices

### ✅ DO:
- Use App Password (not regular password)
- Keep SMTP_PASSWORD in .env (never commit to git)
- Use environment variables in production
- Rotate App Password every 6 months

### ❌ DON'T:
- Don't use your regular Gmail password
- Don't commit .env to GitHub
- Don't share App Password
- Don't disable 2FA after creating App Password

---

## 📊 Email Limits & Scaling

### Gmail Free Tier:
```
Daily Limit: 500 emails
Per User: 4 emails max (4 reminder intervals)
Max Users: 125 users/day
Monthly: ~3,750 users
```

### When to Upgrade:

**If you have > 100 users**:
- Consider SendGrid (100 emails/day free)
- Or upgrade to Google Workspace ($6/user/month, 2000 emails/day)

**If you have > 500 users**:
- Use SendGrid Pro ($19.95/month, 40K emails/month)
- Or AWS SES ($0.10 per 1000 emails)

---

## 🎯 Quick Setup Checklist

- [ ] Gmail account created
- [ ] 2-Step Verification enabled
- [ ] App Password generated
- [ ] SMTP_USER set to your Gmail
- [ ] SMTP_PASSWORD set to App Password (no spaces)
- [ ] SMTP_HOST set to smtp.gmail.com
- [ ] SMTP_PORT set to 587
- [ ] Test email sent successfully
- [ ] Emails not going to spam

---

## 💡 Pro Tips

1. **Use a dedicated email**: Create `noreply@yourdomain.com` for professional look
2. **Monitor sending**: Check Gmail "Sent" folder to track emails
3. **Test regularly**: Send test emails before going live
4. **Backup option**: Configure SendGrid as fallback
5. **Custom domain**: Use custom domain for better deliverability

---

## 📚 Related Documentation

- Gmail App Passwords: https://support.google.com/accounts/answer/185833
- SendGrid Setup: https://sendgrid.com/docs/
- SMTP Troubleshooting: See `NOTIFICATION_SETUP.md`

---

## ✅ Summary

**SMTP_USER** = Your Gmail address that sends reminder emails

**Setup Steps**:
1. Enable 2FA on Gmail
2. Generate App Password
3. Add to environment variables
4. Test email sending
5. Deploy and enjoy! 🎉

**Cost**: ₹0 (Free with Gmail)

---

**Need Help?** Check the troubleshooting section or test with `test_email.py`

**Last Updated**: January 18, 2026
