# Document Expiry Reminder - Frontend

React frontend with Google Cloud Vision OCR integration for smart document scanning.

## Features

- 📸 Smart document scanning with OCR
- 📋 Document management dashboard
- 🔔 Visual expiry status indicators
- 📊 Statistics overview
- 🎨 Modern, responsive UI

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Update `.env` with your backend URL:
```
VITE_API_URL=http://localhost:8000
```

4. Run development server:
```bash
npm run dev
```

App will run on: http://localhost:5173

## Build for Production

```bash
npm run build
```

## Deployment

### Vercel (Recommended)
1. Push code to GitHub
2. Import project on Vercel
3. Add environment variable: `VITE_API_URL=your-backend-url`
4. Deploy

### Netlify
1. Push code to GitHub
2. Connect repository on Netlify
3. Build command: `npm run build`
4. Publish directory: `dist`
5. Add environment variable: `VITE_API_URL=your-backend-url`

## Project Structure

```
src/
├── components/       # React components
│   ├── DocumentScanner.jsx
│   ├── DocumentForm.jsx
│   └── DocumentList.jsx
├── services/        # API services
│   └── api.js
├── config/          # Configuration
│   └── api.js
├── App.jsx          # Main app component
└── main.jsx         # Entry point
```

## Technologies

- React 19
- Vite
- Axios
- React Toastify
