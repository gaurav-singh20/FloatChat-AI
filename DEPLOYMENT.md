# FloatChat-AI Deployment Guide

Your code is now on GitHub! Here's how to deploy it to get a working link.

## 🚀 Quick Deployment Steps

### Option 1: Deploy on Render (Recommended - Free Tier Available)

#### Backend Deployment on Render

1. **Go to [Render.com](https://render.com)** and sign up/login with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select repository: `gaurav-singh20/FloatChat-AI`
   - Click "Connect"

3. **Configure Service**
   - **Name**: `floatchat-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     cd backend && pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     cd backend && gunicorn app:app
     ```

4. **Add Environment Variables** (click "Advanced" → "Add Environment Variable"):
   ```
   AI_MODE=openai
   OPENAI_API_KEY=your_actual_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   DATABASE_URL=sqlite:///./db/argo_data.db
   FLASK_ENV=production
   PORT=10000
   ```
   
   ⚠️ **Important**: Render doesn't support Ollama, so you MUST use OpenAI with API key

5. **Create Service** - Wait 5-10 minutes for deployment

6. **Get Backend URL**: After deployment, copy your service URL (e.g., `https://floatchat-backend.onrender.com`)

#### Frontend Deployment on Vercel

1. **Go to [Vercel.com](https://vercel.com)** and sign up/login with GitHub

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import `gaurav-singh20/FloatChat-AI`

3. **Configure Project**
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Add Environment Variable**:
   ```
   REACT_APP_API_URL=https://floatchat-backend.onrender.com
   ```
   (Replace with your actual Render backend URL from step 6 above)

5. **Deploy** - Takes 2-3 minutes

6. **Get Live URL**: e.g., `https://floatchat-ai.vercel.app`

---

### Option 2: Deploy on Railway (Alternative)

#### Backend on Railway

1. **Go to [Railway.app](https://railway.app)** and login with GitHub

2. **New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `gaurav-singh20/FloatChat-AI`

3. **Configure**
   - **Root Directory**: `backend`
   - **Start Command**: `gunicorn app:app`
   - Add environment variables (same as Render)

4. **Generate Domain** - Click "Settings" → "Generate Domain"

#### Frontend on Netlify

1. **Go to [Netlify.com](https://netlify.com)** and login with GitHub

2. **Add New Site** → "Import from Git"
   - Choose GitHub
   - Select `gaurav-singh20/FloatChat-AI`

3. **Build Settings**:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/build`

4. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-railway-backend.railway.app
   ```

---

## 📝 Post-Deployment Setup

### 1. Update Frontend API URL

After backend is deployed, update `frontend/src/App.jsx`:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
```

This is already in your code, so just make sure you set the environment variable on Vercel/Netlify.

### 2. Populate Database

After backend deployment, you need to add data:

**Option A**: SSH into Render and run:
```bash
python generate_sample_data.py
```

**Option B**: Modify `app.py` to auto-generate sample data on first run:
```python
# Add after Base.metadata.create_all()
from generate_sample_data import generate_sample_data
if not session.query(ArgoRecord).first():
    generate_sample_data()
```

### 3. Test Your Deployment

1. Visit your frontend URL (e.g., `https://floatchat-ai.vercel.app`)
2. Type a question like "What's the average temperature?"
3. If working, you should see AI response!

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: "Application failed to respond"
- **Solution**: Check Render logs for errors
- Make sure `gunicorn` is in `requirements.txt` (✅ already added)

**Problem**: "AI not responding"
- **Solution**: Check OpenAI API key is valid and has credits
- Verify `AI_MODE=openai` in environment variables

**Problem**: "No data available"
- **Solution**: Run `generate_sample_data.py` or modify app.py to auto-generate

### Frontend Issues

**Problem**: "Failed to fetch"
- **Solution**: Make sure `REACT_APP_API_URL` points to your backend URL
- Check CORS is enabled (✅ already configured)

**Problem**: "Module not found"
- **Solution**: Make sure `package.json` is in frontend directory
- Redeploy with correct root directory setting

---

## 💰 Cost Breakdown

### Free Tier Limits

**Render Free Tier**:
- ✅ 750 hours/month (enough for always-on)
- ⚠️ Spins down after 15 min inactivity (first request slow)
- ✅ 512 MB RAM

**Vercel Free Tier**:
- ✅ Unlimited websites
- ✅ 100 GB bandwidth/month
- ✅ No spin-down (always fast)

**OpenAI API**:
- ❌ NOT free - need to add payment method
- 💰 Cost: ~$0.001 per query with gpt-4o-mini
- 💡 Alternative: Use free local testing with Ollama locally, deploy with OpenAI

---

## 🎯 Your Deployed URLs

After following above steps, you'll have:

- **Backend**: `https://floatchat-backend.onrender.com`
- **Frontend**: `https://floatchat-ai.vercel.app`
- **GitHub**: `https://github.com/gaurav-singh20/FloatChat-AI`

Share the frontend URL for your project demonstration! 🎉
