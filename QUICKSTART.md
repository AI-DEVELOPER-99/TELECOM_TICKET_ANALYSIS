# Telecom Ticket Analysis - Quick Start Guide

## ⚡ Quick Setup (5 minutes)

### Step 1: Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Add OpenAI API Key
Edit `backend/.env`:
```
OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Build Vector Store (First Time Only)
```bash
cd backend
source venv/bin/activate
python vector_store.py
```
This takes 2-5 minutes and only needs to be done once.

### Step 4: Start Backend
```bash
# In backend directory with venv activated
python app.py
```
Backend will run on http://localhost:5000

### Step 5: Start Frontend

**Option A - Web UI:**
```bash
# In a new terminal
cd frontend
npm start
```
Open http://localhost:3000

**Option B - CLI:**
```bash
cd frontend
npm run cli
```

## 🎯 Quick Test

### Using CLI:
1. Select "Analyze New Ticket"
2. Subject: `Internet not working`
3. Description: `My internet connection keeps dropping every few minutes`
4. View top 3 solutions!

### Using Web UI:
1. Go to http://localhost:3000
2. Click "Analyze Ticket" tab
3. Enter ticket details
4. Click "Analyze Ticket" button

## 🔧 Troubleshooting

**Backend won't start:**
- Check API key in `backend/.env`
- Ensure Python 3.8+ installed
- Run: `pip install -r requirements.txt`

**Frontend can't connect:**
- Ensure backend is running
- Check http://localhost:5000/health

**Need help?**
- See full documentation in `readme.md`
- Check configuration in `.env` files

## 📚 Key Commands

```bash
# Backend
cd backend
source venv/bin/activate  # Always activate first
python app.py             # Start server
python vector_store.py    # Rebuild index

# Frontend
cd frontend
npm start                 # Start web UI
npm run cli              # Start CLI
```

## 🎨 Features

✅ AI-powered solution suggestions  
✅ Ranked by suitability percentage  
✅ Based on 16,000+ historical tickets  
✅ Modern web interface  
✅ Interactive CLI  
✅ Fast vector search  

---
**For detailed documentation, see readme.md**
