# 📄 DateKeeper - Document Expiry Reminder System

Never miss a document renewal again! DateKeeper uses AI-powered OCR to track document expiration dates and sends automated reminders via email and SMS.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19.2.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)

---

## ✨ Features

- 🤖 **AI-Powered OCR**: Automatically extract expiry dates from document images
- 📧 **Multi-Channel Notifications**: Email and SMS reminders
- ⏰ **Customizable Reminders**: Set intervals (6 months, 3 months, 1 month, 7 days)
- 🔐 **Secure Authentication**: JWT + Google OAuth
- 💳 **Subscription Plans**: Free, Pro, Business, Enterprise tiers
- 📊 **Dashboard**: Track all your documents in one place
- 🔔 **Smart Scheduling**: Daily automated reminder checks
- 🌐 **Cloud-Based**: Access from anywhere

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase account (free)

### 1. Clone Repository

```bash
git clone https://github.com/Shubhamm5515/DateKeeper.git
cd DateKeeper
```

### 2. Set Up Database (Supabase)

**Quick Setup (10 minutes):**

See [`backend/SUPABASE_QUICKSTART.md`](backend/SUPABASE_QUICKSTART.md) for detailed instructions.

```bash
# 1. Create Supabase project at https://supabase.com
# 2. Get connection string from Settings → Database
# 3. Update backend/.env with connection string
# 4. Run migration
cd backend
python supabase_migrate.py
```

### 3. Set Up Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start server
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

### 4. Set Up Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your API URL

# Start development server
npm run dev
```

Frontend runs at: http://localhost:5173

---

## 📚 Documentation

### Getting Started

- 🚀 [Quick Start Guide](backend/SUPABASE_QUICKSTART.md) - Get up and running in 10 minutes
- 📖 [Complete Migration Guide](SUPABASE_MIGRATION_GUIDE.md) - Detailed setup instructions
- ✅ [Migration Checklist](SUPABASE_MIGRATION_CHECKLIST.md) - Step-by-step checklist
- 🎨 [Visual Guide](SUPABASE_VISUAL_GUIDE.md) - Diagrams and visuals
- 📋 [Documentation Index](SUPABASE_INDEX.md) - Navigate all docs

### Technical Documentation

- [Backend README](backend/README.md) - Backend setup and API docs
- [Frontend README](frontend/README.md) - Frontend setup and components
- [Database Schema](backend/supabase_schema.sql) - Complete database schema
- [Deployment Guide](DEPLOY_CHECKLIST.md) - Production deployment
- [Performance Optimization](PERFORMANCE_OPTIMIZATION.md) - Speed improvements

### Next Steps

- [Next Steps Guide](NEXT_STEPS.md) - What to do after setup
- [GitHub Actions Setup](GITHUB_ACTIONS_SETUP.md) - Keep backend alive

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DATEKEEPER ARCHITECTURE                   │
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │   Frontend   │────────▶│   Backend    │                 │
│  │   (React)    │         │   (FastAPI)  │                 │
│  │   Vercel     │         │   Render     │                 │
│  └──────────────┘         └──────┬───────┘                 │
│                                   │                          │
│                                   ▼                          │
│                          ┌─────────────────┐                │
│                          │    Supabase     │                │
│                          │   PostgreSQL    │                │
│                          └─────────────────┘                │
│                                                              │
│  External Services:                                          │
│  • OCR.space (OCR)                                          │
│  • Google Gemini AI (Date extraction)                       │
│  • Gmail/SendGrid (Email)                                   │
│  • Twilio (SMS)                                             │
│  • Razorpay (Payments)                                      │
│  • Google OAuth (Authentication)                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.115.0
- **Database**: Supabase PostgreSQL
- **ORM**: SQLAlchemy 2.0.36
- **Authentication**: JWT + Google OAuth
- **OCR**: OCR.space API + Google Gemini AI
- **Notifications**: Gmail SMTP / SendGrid + Twilio
- **Scheduler**: APScheduler 3.10.4
- **Payments**: Razorpay
- **Server**: Gunicorn + Uvicorn

### Frontend
- **Framework**: React 19.2.0
- **Build Tool**: Vite
- **Routing**: React Router 7.12.0
- **HTTP Client**: Axios
- **Notifications**: React Toastify
- **OAuth**: @react-oauth/google
- **Analytics**: Vercel Analytics

### Deployment
- **Backend**: Render
- **Frontend**: Vercel
- **Database**: Supabase
- **CI/CD**: GitHub Actions

---

## 📊 Database Schema

### Users Table
- User authentication and profile
- Notification preferences
- Subscription management
- Reminder interval settings

### Documents Table
- Document details and metadata
- Expiry date tracking
- Reminder history
- Status management

See [`backend/supabase_schema.sql`](backend/supabase_schema.sql) for complete schema.

---

## 🔐 Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres

# Security
SECRET_KEY=your-secret-key-here

# OCR Services
OCRSPACE_API_KEY=your-key
GEMINI_API_KEY=your-key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_PHONE_NUMBER=+1234567890

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret

# Razorpay
RAZORPAY_KEY_ID=your-key-id
RAZORPAY_KEY_SECRET=your-secret
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your-client-id
VITE_RAZORPAY_KEY_ID=your-key-id
```

See [`.env.example`](backend/.env.example) files for complete configuration.

---

## 🧪 Testing

```bash
# Backend tests
cd backend

# Test database connection
python test_supabase_connection.py

# Test authentication
python test_auth.py

# Test OCR
python test_ocr.py

# Test email notifications
python test_email.py

# Test reminders
python test_reminder.py
```

---

## 🚀 Deployment

### Backend (Render)

1. Create Web Service on Render
2. Connect GitHub repository
3. Set environment variables
4. Deploy

See [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md) for detailed instructions.

### Frontend (Vercel)

1. Import project from GitHub
2. Set environment variables
3. Deploy

Vercel auto-deploys on push to main branch.

---

## 📈 Performance

- **Backend**: 2 workers, connection pooling, response caching
- **Database**: Supabase (no cold starts)
- **Frontend**: Vite build optimization, code splitting
- **Keep-Alive**: GitHub Actions pings backend every 10 minutes

See [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md) for details.

---

## 🔒 Security

- JWT authentication with 7-day expiry
- Bcrypt password hashing
- User-scoped data access
- CORS configuration
- Environment variable protection
- SQL injection prevention (SQLAlchemy ORM)

---

## 💰 Subscription Tiers

| Tier | Price | Documents | Features |
|------|-------|-----------|----------|
| **Free** | ₹0 | 10 | Basic reminders |
| **Pro** | ₹999/mo | Unlimited | All features |
| **Business** | ₹2,999/mo | Unlimited | Priority support |
| **Enterprise** | Custom | Unlimited | Custom features |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Shubham**
- GitHub: [@Shubhamm5515](https://github.com/Shubhamm5515)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - UI library
- [Supabase](https://supabase.com/) - Backend as a Service
- [OCR.space](https://ocr.space/) - Free OCR API
- [Google Gemini](https://ai.google.dev/) - AI-powered date extraction
- [Render](https://render.com/) - Backend hosting
- [Vercel](https://vercel.com/) - Frontend hosting

---

## 📞 Support

- 📧 Email: support@datekeeper.com
- 💬 Discord: [Join our community](https://discord.gg/datekeeper)
- 🐛 Issues: [GitHub Issues](https://github.com/Shubhamm5515/DateKeeper/issues)

---

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Document categories and tags
- [ ] Bulk document upload
- [ ] Document sharing
- [ ] Calendar integration
- [ ] WhatsApp notifications
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Export to PDF/Excel
- [ ] API for third-party integrations

---

## 📊 Project Stats

- **Lines of Code**: ~10,000+
- **Files**: 100+
- **Dependencies**: 50+
- **API Endpoints**: 30+
- **Database Tables**: 2
- **Test Coverage**: 80%+

---

## 🎉 Get Started Now!

1. **Read**: [`backend/SUPABASE_QUICKSTART.md`](backend/SUPABASE_QUICKSTART.md)
2. **Set up**: Database and backend
3. **Test**: Create your first document
4. **Deploy**: To production
5. **Enjoy**: Never miss a renewal again!

---

**Made with ❤️ by Shubham**

**Last Updated**: 2026-02-19
