# FloatChat-AI 🌊

An AI-powered conversational interface for exploring **ARGO Ocean Data**. FloatChat combines real-time oceanographic measurements from autonomous ARGO floats with advanced AI to provide an intuitive way to query and understand ocean data.

![FloatChat Screenshot](https://img.shields.io/badge/React-19.2.0-blue) ![Flask](https://img.shields.io/badge/Flask-3.1.2-green) ![OpenAI](https://img.shields.io/badge/OpenAI-API-orange)

## 🎯 Features

- **AI-Powered Chat Interface**: Natural language queries about oceanographic data
- **ARGO Float Data Integration**: Real-time data from autonomous ocean profiling floats
- **Intelligent Context-Aware Responses**: RAG (Retrieval Augmented Generation) for accurate, data-backed answers
- **Beautiful Modern UI**: Sleek dark-themed chat interface with sidebar navigation
- **Data Visualization Ready**: Built-in support for temperature, salinity, and depth analysis
- **Multi-Chat Support**: Manage multiple conversation threads
- **Persistent Chat History**: Local storage of conversations

## 📊 What is ARGO?

ARGO floats are autonomous oceanographic instruments that:
- Drift with ocean currents at depth
- Profile the water column every 10 days
- Measure **temperature**, **salinity**, and **pressure/depth**
- Transmit data via satellite
- Cover all major ocean basins globally

This project focuses on **Indian Ocean** data but can be extended to any region.

## 🏗️ Project Structure

```
FloatChat-AI/
├── backend/
│   ├── app.py                  # Flask API server
│   ├── fetch_argovis.py        # Data fetching script
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment configuration
│   ├── db/
│   │   ├── models.py          # SQLAlchemy models
│   │   └── session.py         # Database session
│   └── services/
│       ├── ai_service.py      # OpenAI integration & RAG
│       └── data_service.py    # Data query engine
│
└── frontend/
    ├── package.json            # Node dependencies
    ├── public/
    └── src/
        ├── App.jsx            # Main React component
        ├── index.jsx          # React entry point
        ├── App.css
        └── index.css          # Styling
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (with pip)
- **Node.js 16+** (with npm)
- **Ollama** (FREE local AI - download at [ollama.ai](https://ollama.ai)) **RECOMMENDED**
- *Optional:* OpenAI API Key (get one at [platform.openai.com](https://platform.openai.com))
- Internet connection (for fetching ARGO data)

### Step 1: Clone and Setup

```bash
# Navigate to your project directory
cd FloatChat-AI
```

### Step 2: Install Ollama (Recommended - FREE)

```bash
# Download and install Ollama from: https://ollama.ai/download
# After installation, pull the AI model:
ollama pull llama3.2
```

### Step 3: Backend Setup

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configuration is ready! (Ollama is already set as default in .env)
# Optional: To use OpenAI instead, edit backend/.env:
# AI_MODE=openai
# OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 4: Fetch ARGO Data

```bash
# Still in backend directory with venv activated
python fetch_argovis.py
```

This will:
- Fetch data from ARGO float 2902746 (Indian Ocean)
- Store it in SQLite database (`argo.db`)
- Save a CSV backup in `data/` folder

### Step 5: Start Backend Server

```bash
# Start Flask API server
python app.py
```

You should see:
```
🌊 FloatChat-AI Server starting on http://127.0.0.1:5000
🔍 Debug mode: True
```

Keep this terminal running!

### Step 6: Frontend Setup (New Terminal)

```bash
# Open a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

The app will open automatically at `http://localhost:3000`

## 🎮 Usage

### AI-Powered Queries (with Ollama)

Try asking FloatChat:

- "What is the average temperature in the dataset and how does it vary with depth?"
- "Explain the relationship between depth and temperature"
- "Tell me about ocean stratification in this data"
- "Compare surface water characteristics with deep water"
- "What can you tell me about the thermocline?"

### AI Modes

**With Ollama (Default - FREE):**
- ✅ Full AI-powered conversational responses
- ✅ Unlimited queries, no API costs
- ✅ Runs locally on your machine
- ✅ Fast responses after first load

**With OpenAI (Optional):**
- Full AI-powered responses using GPT-4o-mini
- Requires API key and credits
- Set `AI_MODE=openai` in `.env`

**Fallback Mode (No AI):**
- Rule-based responses with statistics
- Data summaries and ranges
- Basic query responses

## 🔧 Configuration

### Backend Configuration (`backend/.env`)

```env
# Database
DB_URL=sqlite:///argo.db

# Flask Server
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True

# AI Configuration
AI_MODE=ollama  # Use 'ollama' (free) or 'openai' (requires credits)

# Ollama Configuration (FREE - Default)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# OpenAI Configuration (Optional)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# ARGO Float Configuration
FLOAT_ID=2902746
```

### Frontend Configuration

The frontend proxies API requests to `http://127.0.0.1:5000` (configured in `package.json`).

## 📡 API Endpoints

### `POST /api/chat`

Main chat endpoint for AI responses.

**Request:**
```json
{
  "message": "What is the average temperature?"
}
```

**Response:**
```json
{
  "reply": "Based on the ARGO float data, the average temperature is..."
}
```

### `GET /api/data/stats`

Get dataset statistics.

**Response:**
```json
{
  "total_records": 1523,
  "floats": ["2902746"],
  "temperature": {"min": 10.2, "max": 29.8, "avg": 18.5},
  "salinity": {"min": 34.1, "max": 35.9, "avg": 34.8},
  ...
}
```

### `POST /api/data/query`

Query ARGO data with filters.

## 🛠️ Development

### Adding New ARGO Floats

Edit `backend/.env`:
```env
FLOAT_ID=2902746  # Change to another float ID
```

Run `python fetch_argovis.py` to ingest new data.

### Customizing AI Behavior

Edit the system prompt in `backend/services/ai_service.py`:

```python
def _build_system_prompt(self):
    return """You are FloatChat, an expert oceanographic AI..."""
```

### Database Schema

**ArgoRecord** table:
- `id`: Primary key
- `time`: Measurement timestamp
- `latitude`, `longitude`: Geographic position
- `depth`: Pressure in decibars
- `temperature`: Water temperature (°C)
- `salinity`: Salinity (PSU)
- `platform`: Float WMO number

## 🐛 Troubleshooting

### Backend won't start

```bash
# Make sure venv is activated
cd backend
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### No data in database

```bash
# Fetch ARGO data
cd backend
python fetch_argovis.py
```

### Frontend can't connect to backend

1. Ensure backend is running on `http://127.0.0.1:5000`
2. Check `frontend/package.json` has `"proxy": "http://127.0.0.1:5000"`
3. Restart frontend: `npm start`

### AI Response Issues

**Using Ollama:**
1. Ensure Ollama is running: `ollama list` should show llama3.2
2. First query may take 10-20 seconds (model loading)
3. Subsequent queries will be much faster

**Using OpenAI:**
1. Verify API key in `backend/.env`
2. Check your OpenAI account has credits
3. Set `AI_MODE=openai` in `.env`

**Slow Responses:**
- Ollama first query loads the model (one-time delay)
- Keep Ollama running in the background for best performance

## 📚 Technology Stack

**Backend:**
- Flask 3.1.2 - Web framework
- SQLAlchemy 2.0.44 - ORM
- Ollama (llama3.2) - Local AI (default)
- OpenAI API - Cloud AI (optional)
- Pandas - Data processing
- netCDF4 - Ocean data format support

**Frontend:**
- React 19.2.0 - UI framework
- Modern ES6+ JavaScript
- CSS3 with custom properties
- Local storage for persistence

**Database:**
- SQLite - Lightweight embedded database

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

- [ ] Add data visualization charts (Plotly integration)
- [ ] Support multiple ARGO floats simultaneously
- [ ] Add geographic map view
- [ ] Export chat conversations
- [ ] Advanced filtering and search
- [ ] Historical data comparison

## 📝 License

MIT License - feel free to use this project for learning and development.

## 🌟 Acknowledgments

- **ARGO Program**: Global array of profiling floats (argovis.colorado.edu)
- **OpenAI**: GPT models for conversational AI
- **React**: UI framework
- **Flask**: Python web framework

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Built with 🌊 for ocean data exploration**
