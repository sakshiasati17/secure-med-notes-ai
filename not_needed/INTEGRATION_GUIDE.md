# 🚀 Integration Guide: React Frontend + FastAPI Backend

This guide will help you integrate the premium React frontend with the existing FastAPI backend and Streamlit UI.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Quick Start](#quick-start)
3. [Running Both UIs](#running-both-uis)
4. [API Integration Details](#api-integration-details)
5. [Streamlit Theme Updates](#streamlit-theme-updates)
6. [Deployment Options](#deployment-options)

---

## 🏗️ Architecture Overview

```
secure-med-notes-ai/
├── api/                          # FastAPI Backend (Port 8000)
│   ├── main.py                   # CORS enabled for React
│   ├── routes/                   # API endpoints
│   └── services/ai_service.py    # AI integration
│
├── ui/                           # Streamlit UI (Port 8501)
│   ├── app.py                    # Original Streamlit app
│   └── pages/                    # Doctor/Nurse pages
│
├── Design Premium Landing Page/  # React UI (Port 3000) ✨ NEW
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── services/api.ts       # API client
│   │   └── App.tsx              # Main app
│   └── package.json
│
└── docker-compose.yml            # PostgreSQL + Redis
```

### Data Flow

```
┌─────────────┐        ┌──────────────┐        ┌─────────────┐
│   React UI  │───────▶│  FastAPI     │───────▶│  PostgreSQL │
│  (Port 3000)│◀───────│  (Port 8000) │◀───────│  (Port 5434)│
└─────────────┘        └──────────────┘        └─────────────┘
                              │
                              │
                              ▼
                       ┌──────────────┐
                       │   OpenAI API │
                       │  (AI Service)│
                       └──────────────┘

┌─────────────┐        ┌──────────────┐
│ Streamlit UI│───────▶│  FastAPI     │
│  (Port 8501)│◀───────│  (Port 8000) │
└─────────────┘        └──────────────┘
```

---

## ⚡ Quick Start

### Step 1: Start Infrastructure

```bash
# Start PostgreSQL and Redis
docker compose up -d

# Verify services are running
docker compose ps
```

### Step 2: Setup Python Environment

```bash
# Create/activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Seed Database

```bash
# Create tables and seed data
python api/seed_more_data.py
```

### Step 4: Start FastAPI Backend

```bash
# Terminal 1: Start API server
uvicorn api.main:app --reload --port 8000

# Verify API is running
# Open http://localhost:8000/docs
```

### Step 5: Start React Frontend

```bash
# Terminal 2: Navigate to React app
cd "Design Premium Landing Page"

# Install Node dependencies
npm install

# Start development server
npm run dev

# App opens at http://localhost:3000
```

### Step 6: (Optional) Start Streamlit UI

```bash
# Terminal 3: Start Streamlit
streamlit run ui/app.py --server.port 8501

# App opens at http://localhost:8501
```

---

## 🎯 Running Both UIs

You can run both React and Streamlit UIs simultaneously. They both connect to the same FastAPI backend and database.

### Use Cases

- **React UI**: Modern, premium landing page and dashboards with animations
- **Streamlit UI**: Quick prototyping, data analysis, internal tools

### Ports Summary

| Service | Port | URL |
|---------|------|-----|
| React UI | 3000 | http://localhost:3000 |
| FastAPI | 8000 | http://localhost:8000 |
| Streamlit | 8501 | http://localhost:8501 |
| PostgreSQL | 5434 | localhost:5434 |
| Redis | 6379 | localhost:6379 |

---

## 🔌 API Integration Details

### CORS Configuration

The FastAPI backend needs CORS enabled for React. Check `api/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Authentication Flow

1. **Login**: User enters credentials in React app
2. **API Call**: `POST /auth/login` with email/password
3. **Response**: Backend returns JWT access token
4. **Storage**: Token stored in LocalStorage
5. **Subsequent Requests**: Token sent in `Authorization: Bearer <token>` header

### API Client (React)

The React app uses a centralized API service (`src/services/api.ts`):

```typescript
import { api } from '../services/api';

// Login
await api.login(email, password);

// Get patients
const patients = await api.getPatients();

// Create note
const note = await api.createNote({
  patient_id: 1,
  title: "Progress Note",
  content: "Patient doing well...",
  note_type: "DOCTOR_NOTE"
});

// AI Summarization
const summary = await api.summarizeNote(noteId);
```

---

## 🎨 Streamlit Theme Updates

To match the React design in Streamlit, update `ui/design_system.py`:

### Color Palette

The React app uses:
- Primary: Purple to Indigo gradient
- Accent (Doctor): Purple `#667eea`
- Accent (Nurse): Pink `#ec4899`

### Suggested Updates

```python
# In ui/design_system.py

# Update CSS variables
BASE_CSS = """
    <style>
        :root {
            --gradient-start: #667eea;  /* Purple */
            --gradient-end: #764ba2;    /* Indigo */
            --nurse-accent: #ec4899;    /* Pink */
            --doctor-accent: #667eea;   /* Purple */
            ...
        }
    </style>
"""
```

### Adding Emojis to Streamlit

```python
# In ui/pages/nurse/dashboard.py

st.markdown("## 👋 Good Morning, Nurse!")
st.markdown("### 👥 My Patients Today")
st.markdown("### 💉 Vitals Due")
st.markdown("### 💊 Medications")
```

---

## 🚀 Deployment Options

### Option 1: Deploy React as Main UI

**Replace Streamlit completely with React frontend**

Pros:
- Modern, professional UI
- Better performance
- Mobile-friendly

Steps:
1. Build React for production: `npm run build`
2. Serve static files with FastAPI or Nginx
3. Update API CORS for production domain

### Option 2: Hybrid Deployment

**Use React for landing page, Streamlit for internal tools**

Pros:
- Best of both worlds
- Quick development with Streamlit
- Professional public-facing UI

Setup:
- React at `/` (root)
- Streamlit at `/internal` or subdomain
- Nginx reverse proxy configuration

### Option 3: Keep Both Separate

**Run React and Streamlit on different ports/domains**

Pros:
- No changes needed
- Easy to switch between UIs
- Independent development

Current setup - already working!

---

## 📝 Environment Variables

### React (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
```

### FastAPI (.env)

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5434/mednotes
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-your-openai-api-key
```

---

## 🧪 Testing the Integration

### Test Authentication

1. Open React app: http://localhost:3000
2. Click "Login to Get Started"
3. Use Quick Login or enter:
   - Email: `dr.williams@hospital.com`
   - Password: `password123`
4. Should redirect to Doctor Dashboard

### Test API Connection

1. Open browser DevTools (F12)
2. Go to Network tab
3. Login to React app
4. Check for requests to `http://localhost:8000/auth/login`
5. Should see 200 status with access_token

### Test Data Flow

1. Login as doctor
2. Navigate to Patients tab
3. Should see list of patients from database
4. Create a new note
5. Verify note appears in Streamlit UI and database

---

## 🐛 Common Issues & Solutions

### Issue: "Cannot connect to API"

**Solution:**
```bash
# Check if FastAPI is running
curl http://localhost:8000/docs

# If not, start it
uvicorn api.main:app --reload --port 8000
```

### Issue: "CORS error in browser console"

**Solution:**
Update `api/main.py`:
```python
allow_origins=["http://localhost:3000", "http://localhost:8501"]
```

### Issue: "Login works but data doesn't load"

**Solution:**
```bash
# Check database has data
python api/seed_more_data.py

# Verify in psql
docker exec -it <postgres-container> psql -U postgres -d mednotes
SELECT COUNT(*) FROM patients;
```

### Issue: "npm install fails"

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

## 📊 Performance Optimization

### React Production Build

```bash
# Build optimized bundle
npm run build

# Serve with FastAPI
# Add to api/main.py:
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="Design Premium Landing Page/build", html=True))
```

### Caching Strategy

- **LocalStorage**: JWT tokens
- **React Query**: API response caching (future enhancement)
- **Service Worker**: Offline support (future enhancement)

---

## 🎓 Next Steps

### Immediate
1. ✅ Run `npm install` in React folder
2. ✅ Start all services (Docker, FastAPI, React)
3. ✅ Test login with demo credentials
4. ✅ Explore both dashboards

### Short Term
- Connect Patients Tab to real API data
- Implement Clinical Notes creation with AI
- Add Calendar/Appointments functionality
- Enhance error handling

### Long Term
- Deploy to production (AWS/Azure/GCP)
- Add unit tests (Jest/Vitest)
- Implement E2E tests (Playwright)
- Add monitoring and analytics

---

## 🤝 Support

For issues or questions:
1. Check browser console for errors
2. Check FastAPI logs in terminal
3. Verify all services are running
4. Review this integration guide

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Happy Coding! 🎉**
