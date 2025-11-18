# 🚀 FloatChat-AI Quick Start Guide

## ✅ Your App is Ready!

Everything is configured and working. Here's how to use it:

---

## 🎯 Starting the Application

### 1. Start Backend (if not running)
```powershell
cd "C:\Users\kg it\OneDrive\Desktop\FloatChat-AI\backend"
python app.py
```

**You should see:**
```
✅ Ollama connected successfully
🤖 Using local model: llama3.2
🌊 FloatChat-AI Server starting on http://127.0.0.1:5000
```

### 2. Start Frontend (if not running)
```powershell
cd "C:\Users\kg it\OneDrive\Desktop\FloatChat-AI\frontend"
npm start
```

**Browser opens automatically at:** http://localhost:3000

---

## 💬 Example Questions to Ask

### Temperature Analysis
- "What is the average temperature in the Indian Ocean and how does it vary with depth?"
- "Explain why water temperature decreases as depth increases"
- "At what depth does the thermocline occur?"

### Salinity Questions
- "How does salinity change with depth?"
- "What is the relationship between temperature and salinity?"
- "Explain why ocean salinity is important"

### Ocean Science
- "Explain ocean stratification based on this data"
- "What can you tell me about the mixed layer depth?"
- "Compare surface water with deep water characteristics"

### Data Overview
- "Give me a summary of all measurements"
- "What depth range is covered?"
- "Show me the geographic area of this data"

---

## 🤖 AI Configuration

### Current Setup (Default)
- **Mode:** Ollama (FREE local AI)
- **Model:** llama3.2
- **Cost:** $0 - completely free
- **Limits:** None - unlimited queries

### Response Times
- **First query:** 10-20 seconds (model loading)
- **Subsequent queries:** 2-5 seconds
- **Tip:** Keep Ollama running for best performance

### Switch to OpenAI (Optional)

Edit `backend/.env`:
```env
AI_MODE=openai
OPENAI_API_KEY=sk-your-actual-key
```

Then restart backend.

---

## 📊 Your Data

- **Float ID:** 2902746
- **Location:** Indian Ocean (~10°S, 75°E)
- **Records:** 150 measurements
- **Depth Range:** 5 - 2000 dbar
- **Temperature:** 1.21 - 28.39°C
- **Salinity:** 34.22 - 35.22 PSU

---

## 🎨 Using the Interface

### Chat Features
- **New Chat:** Click "+ New chat" button
- **Switch Chats:** Click on chat items in sidebar
- **Rename Chat:** Click on title in main area
- **Delete Chat:** Click X button on chat item
- **Auto-save:** All chats saved in browser

### Tips
- Use specific questions for better AI responses
- Ask follow-up questions in the same chat
- Create new chats for different topics
- Chat history persists across sessions

---

## 🔧 Common Tasks

### Add More Data
```powershell
cd backend
python fetch_argovis.py  # Fetch real data (needs internet)
# OR
python generate_sample_data.py  # Generate test data
```

### Change ARGO Float
Edit `backend/.env`:
```env
FLOAT_ID=different_float_id
```

Then run `fetch_argovis.py`

### View Database Stats
Visit: http://127.0.0.1:5000/api/data/stats

### Check Server Health
Visit: http://127.0.0.1:5000/

---

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check if Python virtual environment is activated
cd backend
.venv\Scripts\activate  # Windows
python app.py
```

### AI responses are slow
- **First query:** Normal (model loading)
- **Always slow:** Check if Ollama is running: `ollama list`
- **Restart Ollama:** Close and reopen Ollama app

### Frontend can't connect
1. Ensure backend is running on port 5000
2. Check `frontend/package.json` has proxy configured
3. Restart both servers

### No data responses
```powershell
cd backend
python generate_sample_data.py  # Regenerate data
```

---

## 📚 Documentation Files

- **README.md** - Complete project overview
- **STARTUP_GUIDE.md** - Detailed setup instructions
- **BUILD_SUMMARY.md** - Technical implementation details
- **QUICK_START.md** - This file (quick reference)

---

## 🎉 Enjoy Your AI Oceanography Assistant!

You now have a fully functional AI chatbot that understands oceanographic data!

**Key Features:**
- 🌊 Real ARGO float data analysis
- 🤖 FREE unlimited AI responses
- 📊 Statistical analysis
- 💬 Natural language queries
- 🔒 Private (runs locally)
- ⚡ Fast responses

**Have fun exploring ocean data!** 🚀
