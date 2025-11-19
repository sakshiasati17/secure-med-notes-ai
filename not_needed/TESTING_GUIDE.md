# Testing Guide - Secure Medical Notes AI

## 🚀 Quick Start (Everything Running)

### Current Status:
- ✅ **PostgreSQL**: Running on port 5434
- ✅ **Redis**: Running on port 6379
- ✅ **FastAPI Backend**: Running on port 8000
- ✅ **React Frontend**: Running on port 3000

### Access URLs:
- **React App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Streamlit** (if needed): `streamlit run old_ui/app.py`

---

## 👤 Demo Credentials

### Doctors:
```
Email: dr.williams@hospital.com
Password: password123

Email: dr.chen@hospital.com
Password: password123

Email: dr.patel@hospital.com
Password: password123
```

### Nurses:
```
Email: nurse.davis@hospital.com
Password: password123

Email: nurse.martinez@hospital.com
Password: password123

Email: nurse.lee@hospital.com
Password: password123
```

---

## 🧪 Testing Clinical Notes (PRIMARY FIX)

### React Portal (http://localhost:3000)

1. **Login**:
   - Go to http://localhost:3000
   - Click "Doctor Login" or use quick login button
   - Or enter: dr.williams@hospital.com / password123

2. **Navigate to Clinical Notes Tab**:
   - Click on "Clinical Notes" in the main tabs

3. **Test Compose Tab**:
   - ✅ Select a patient from dropdown
   - ✅ Choose a note template (Progress Note, Admission Note, etc.)
   - ✅ Fill in chief complaint
   - ✅ Fill in template fields (Subjective, Objective, Assessment, Plan)
   - ✅ Click "Save Note"
   - ✅ Verify success message appears
   - ✅ Check that form resets after save

4. **Test Library Tab**:
   - ✅ Click "Notes Library"
   - ✅ Verify all notes are displayed
   - ✅ Check that each note shows:
     - Title
     - Patient name (NOT patient ID)
     - Author name (NOT author ID)
     - Created date
     - Risk level badge (if available)
     - Summary text (if available)
   - ✅ Verify note count is displayed

5. **Test Search Tab**:
   - ✅ Click "Search"
   - ✅ Enter search term (try patient name, author name, or content keyword)
   - ✅ Verify filtered results appear
   - ✅ Check result count updates
   - ✅ Try empty search (should show all notes)

### Streamlit Portal

1. **Start Streamlit**:
   ```bash
   streamlit run old_ui/app.py
   ```

2. **Login**:
   - Open http://localhost:8501
   - Enter: dr.williams@hospital.com / password123

3. **Test Clinical Documentation Studio**:
   - Navigate to "Clinical Documentation Studio" page
   - **Compose Note Tab**:
     - Fill in SOAP note fields
     - Click "💾 Save Clinical Note"
     - Verify success message
     - Page should auto-refresh
   - **Notes Library Tab**:
     - Verify notes are displayed
     - Check patient ID and dates
   - **Search Tab**:
     - Enter keywords
     - Click "Run Search"
     - Verify results

---

## 🔍 Testing Other Features

### Patients Tab:
- ✅ View all patients
- ✅ Search by ID or name
- ✅ View patient statistics
- ⚠️  Note: Patient notes display may have issues (see FIXES_APPLIED.md)

### AI Analytics Tab:
- View AI-generated summaries
- Check risk reports
- Test high-risk patient filtering

### Calendar Tab:
- View appointments
- Create new appointments
- Check appointment scheduling

---

## 🧰 Manual API Testing

### Get Authentication Token:
```bash
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"dr.williams@hospital.com","password":"password123"}' | jq -r .access_token)

echo "Token: $TOKEN"
```

### Test Notes Endpoint:
```bash
# Get all notes
curl -X GET "http://localhost:8000/notes/" \
  -H "Authorization: Bearer $TOKEN" | jq .

# Create a note
curl -X POST "http://localhost:8000/notes/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "title": "Test Note",
    "content": "Test content",
    "note_type": "doctor_note"
  }' | jq .
```

### Test Patients Endpoint:
```bash
curl -X GET "http://localhost:8000/patients/" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### Test AI Endpoints:
```bash
# Get risk report for patient
curl -X GET "http://localhost:8000/ai/risk-report/1" \
  -H "Authorization: Bearer $TOKEN" | jq .

# Check AI status
curl -X GET "http://localhost:8000/ai/ai-status" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

---

## ✅ Expected Behaviors

### Clinical Notes - Library Tab:
```
Should display:
- ✅ Note title
- ✅ Patient name (e.g., "Emily Rodriguez")
- ✅ Author name (e.g., "Dr. Michael Chen")
- ✅ Created timestamp
- ✅ Risk level badge (if assessed)
- ✅ Summary text (if generated)
- ✅ Proper formatting and styling
```

### Clinical Notes - Search:
```
Should search across:
- ✅ Note title
- ✅ Note summary
- ✅ Note type
- ✅ Patient name
- ✅ Author name
```

### Clinical Notes - Creation:
```
Should:
- ✅ Accept all form fields
- ✅ Save to database
- ✅ Show success message
- ✅ Reset form after save
- ✅ Refresh notes list
- ✅ Handle errors gracefully
```

---

## 🐛 Known Issues & Workarounds

### 1. TypeScript Errors in IDE
**Status**: Cosmetic issue, doesn't affect runtime
**Workaround**: Ignore IDE errors, app runs fine

### 2. PatientsTab getPatientNotes()
**Status**: Needs refactoring
**Workaround**: Patient list works, but note display may show wrong data
**See**: FIXES_APPLIED.md for details

### 3. AI Features Require OpenAI API Key
**Status**: Expected behavior
**Workaround**: Set `OPENAI_API_KEY` in `.env` file

---

## 📊 System Health Checks

### Check API Status:
```bash
curl http://localhost:8000/docs
# Should return OpenAPI documentation page
```

### Check Database:
```bash
docker ps | grep postgres
# Should show running PostgreSQL container
```

### Check Redis:
```bash
docker ps | grep redis
# Should show running Redis container
```

### View API Logs:
```bash
tail -f api.log
```

### View React Logs:
```bash
tail -f frontend.log
```

---

## 🔄 Restart Services

### Restart API:
```bash
pkill -f "uvicorn api.main"
source .venv/bin/activate
uvicorn api.main:app --reload --port 8000
```

### Restart React:
```bash
pkill -f "vite"
cd frontend
npm run dev
```

### Restart Docker Services:
```bash
docker compose down
docker compose up -d
```

---

## ✨ What Was Fixed

See [FIXES_APPLIED.md](FIXES_APPLIED.md) for comprehensive list of all fixes.

**Key Fixes:**
1. ✅ Clinical Notes React component now uses correct `NoteSummary` type
2. ✅ Notes display patient names and author names instead of IDs
3. ✅ Streamlit endpoint consistency fixed
4. ✅ Search functionality enhanced with all relevant fields
5. ✅ Better error handling and user feedback

---

## 📝 Next Steps for Full Production

1. **Complete PatientsTab refactoring** for `getPatientNotes()`
2. **Audit remaining tabs**: AI Analytics, Calendar, Tasks
3. **Add comprehensive error boundaries** in React
4. **Implement loading states** for all async operations
5. **Add unit tests** for critical components
6. **Set up E2E tests** with Playwright or Cypress
7. **Configure CI/CD** pipeline
8. **Add monitoring** and logging (Sentry, LogRocket)

---

## 🎉 Happy Testing!

If you encounter any issues, check:
1. [FIXES_APPLIED.md](FIXES_APPLIED.md) - for known fixes
2. `api.log` - for backend errors
3. `frontend.log` - for React errors
4. Browser console - for frontend JavaScript errors
