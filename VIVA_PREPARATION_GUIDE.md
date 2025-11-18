# FloatChat-AI: Complete Technical Guide & Viva Preparation

**A Comprehensive Learning Resource for Understanding Every Aspect of the Project**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack Explained](#technology-stack-explained)
3. [Project Architecture](#project-architecture)
4. [File Structure & Responsibilities](#file-structure--responsibilities)
5. [Database Layer - Deep Dive](#database-layer---deep-dive)
6. [Backend Services - Detailed Explanation](#backend-services---detailed-explanation)
7. [Frontend - React Application](#frontend---react-application)
8. [AI Integration - The Brain](#ai-integration---the-brain)
9. [Key Concepts & Patterns](#key-concepts--patterns)
10. [Code Walkthrough with Examples](#code-walkthrough-with-examples)
11. [How Everything Works Together](#how-everything-works-together)
12. [Common Viva Questions & Answers](#common-viva-questions--answers)
13. [Troubleshooting Guide](#troubleshooting-guide)

---

## 1. Project Overview

### What is FloatChat-AI?

FloatChat-AI is an **AI-powered conversational assistant** for exploring oceanographic data from ARGO floats. Think of it as "ChatGPT for ocean data" - users can ask questions in plain English and get intelligent answers based on real scientific data.

### The Problem We're Solving

**Traditional Approach:**
- Scientists visit complex data portals
- Download large CSV/NetCDF files
- Write custom Python/MATLAB scripts
- Manually analyze and visualize data
- **Time-consuming and requires programming expertise**

**Our Solution:**
- Simple chat interface (like WhatsApp)
- Type questions in natural language
- Get instant, data-backed answers
- **No coding required!**

### Real-World Use Cases

1. **Students:** "What's the average temperature at 100m depth?"
2. **Researchers:** "Show me salinity trends for float 2902746"
3. **Educators:** "Explain the temperature profile of this region"

---

## 2. Technology Stack Explained

### Why We Chose Each Technology

#### **Frontend: React**
- **What:** JavaScript library for building user interfaces
- **Why:** 
  - Creates dynamic, responsive web pages
  - Component-based (reusable code blocks)
  - Large community and excellent documentation
  - Fast rendering with Virtual DOM
- **Alternative:** Vue.js, Angular (we chose React for its simplicity)

#### **Backend: Flask (Python)**
- **What:** Lightweight web framework for Python
- **Why:**
  - Easy to learn and quick to develop
  - Perfect for creating REST APIs
  - Python ecosystem (great for data science)
  - Minimal boilerplate code
- **Alternative:** Django, FastAPI, Express.js (Node.js)

#### **Database: SQLite + SQLAlchemy**
- **SQLite:**
  - **What:** File-based relational database
  - **Why:** Simple, no server setup, perfect for development
  - **Alternative:** PostgreSQL, MySQL (for production scale)

- **SQLAlchemy:**
  - **What:** Object-Relational Mapper (ORM)
  - **Why:** Write Python instead of SQL queries
  - **Benefit:** Code is cleaner and more maintainable

#### **AI Engine: Ollama (Llama 3.2)**
- **What:** Local AI model runner (runs LLMs on your computer)
- **Why:**
  - **Free** (no API costs)
  - **Private** (data stays on your machine)
  - **No internet required** (after initial setup)
- **Alternative:** OpenAI API, Google Gemini (cost money)

---

## 3. Project Architecture

### Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT TIER                          │
│  (React Frontend - Runs in Web Browser)                │
│  - User Interface                                       │
│  - Chat Window                                          │
│  - Data Display                                         │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP Requests (AJAX/Fetch API)
                 ▼
┌─────────────────────────────────────────────────────────┐
│               APPLICATION TIER                          │
│  (Flask Backend - Python API Server)                   │
│  ┌─────────────────────────────────────────────────┐  │
│  │ app.py (Main Routes)                            │  │
│  ├─────────────────────────────────────────────────┤  │
│  │ ai_service.py (AI Logic + RAG)                  │  │
│  ├─────────────────────────────────────────────────┤  │
│  │ data_service.py (Database Queries)              │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────┘
                 │ SQL Queries (via SQLAlchemy)
                 ▼
┌─────────────────────────────────────────────────────────┐
│                    DATA TIER                            │
│  (SQLite Database - argo.db)                           │
│  - ArgoData table                                       │
│  - Temperature, Salinity, Pressure readings            │
└─────────────────────────────────────────────────────────┘
```

### Why This Architecture?

1. **Separation of Concerns:** Each tier has a specific job
2. **Scalability:** Can upgrade/replace individual tiers
3. **Maintainability:** Easy to debug and update
4. **Industry Standard:** Used by major companies

---

## 4. File Structure & Responsibilities

### Backend Files

```
backend/
├── app.py                    # 🚀 Main Flask application (API routes)
├── .env                      # 🔐 Configuration (secrets, API keys)
├── requirements.txt          # 📦 Python dependencies list
├── fetch_argovis.py         # 🌊 Fetches real data from Argovis API
├── generate_sample_data.py  # 🎲 Creates synthetic ARGO data
├── indian_ocean_argo.csv    # 📊 Raw data file
│
├── db/
│   ├── models.py            # 🗄️ Database schema (table definitions)
│   ├── session.py           # 🔌 Database connection manager
│   └── argo.db              # 💾 SQLite database file
│
└── services/
    ├── ai_service.py        # 🧠 AI logic (Ollama integration)
    └── data_service.py      # 📈 Data retrieval functions
```

### Frontend Files

```
frontend/
├── package.json             # 📦 Node.js dependencies
├── public/
│   └── index.html          # 🌐 Main HTML file
│
└── src/
    ├── index.jsx           # 🚪 Entry point (loads App)
    ├── App.jsx             # 🎨 Main React component (chat UI)
    ├── App.css             # 💅 Styling
    └── index.css           # 💅 Global styles
```

---

## 5. Database Layer - Deep Dive

### What is a Database Model?

A **model** is like a blueprint for a database table. It defines what data we store and how.

### Our Database Schema

**File:** `backend/db/models.py`

```python
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ArgoData(Base):
    __tablename__ = 'argo_data'
    
    # Primary key (unique ID for each row)
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Float identifier
    float_id = Column(String, nullable=False, index=True)
    
    # Measurement data
    temperature = Column(Float, nullable=True)
    salinity = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    
    # Location data
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Time of measurement
    timestamp = Column(DateTime, nullable=True, index=True)
```

### Code Explanation (Line by Line)

**Line 1-2:** Import necessary components from SQLAlchemy
- `Column`: Represents a database column
- `Integer, Float, String, DateTime`: Data types
- `declarative_base`: Creates base class for models

**Line 4:** `Base = declarative_base()`
- Creates a base class that all models inherit from
- Provides SQLAlchemy magic methods

**Line 6:** `class ArgoData(Base):`
- Defines our data model
- Inherits from `Base` to get database superpowers

**Line 7:** `__tablename__ = 'argo_data'`
- Sets the actual table name in the database
- Python class name can differ from table name

**Line 10:** `id = Column(Integer, primary_key=True, autoincrement=True)`
- **primary_key=True:** Makes this the unique identifier
- **autoincrement=True:** Database automatically assigns 1, 2, 3...
- Think of it like roll numbers in a class

**Line 13:** `float_id = Column(String, nullable=False, index=True)`
- **String:** Text data type
- **nullable=False:** Must have a value (required field)
- **index=True:** Creates an index for faster searches
  - Like an index in a textbook - helps find data quickly

**Line 16-18:** Temperature, Salinity, Pressure
- **Float:** Decimal numbers (e.g., 15.7°C)
- **nullable=True:** Can be empty (optional)
- Why optional? Some measurements might fail or be unavailable

**Line 21-22:** Latitude, Longitude
- Geographic coordinates
- Example: (20.5°N, 70.3°E)

**Line 25:** `timestamp = Column(DateTime, nullable=True, index=True)`
- **DateTime:** Stores date and time
- **index=True:** Fast searching by date

### Why Use an ORM (SQLAlchemy)?

**Without ORM (Raw SQL):**
```sql
SELECT * FROM argo_data WHERE float_id = '2902746' AND temperature > 20;
```

**With ORM (Python):**
```python
session.query(ArgoData).filter(
    ArgoData.float_id == '2902746',
    ArgoData.temperature > 20
).all()
```

**Benefits:**
1. Write Python instead of SQL
2. Type safety (catch errors before runtime)
3. Database-agnostic (easy to switch from SQLite to PostgreSQL)
4. Automatic query optimization

---

## 6. Backend Services - Detailed Explanation

### Service Layer Pattern

**What:** Separate business logic from routes
**Why:** Keeps code organized and reusable

### Data Service (`backend/services/data_service.py`)

**Purpose:** All database operations live here

```python
from db.models import ArgoData
from db.session import get_session
from sqlalchemy import func

class DataService:
    def __init__(self):
        """Initialize the service with a database session"""
        self.session = get_session()
    
    def get_stats(self):
        """Get overall statistics about the dataset"""
        # Count total measurements
        total_count = self.session.query(ArgoData).count()
        
        # Count unique floats
        unique_floats = self.session.query(
            func.count(func.distinct(ArgoData.float_id))
        ).scalar()
        
        # Calculate average temperature
        avg_temp = self.session.query(
            func.avg(ArgoData.temperature)
        ).scalar()
        
        return {
            'total_measurements': total_count,
            'unique_floats': unique_floats,
            'average_temperature': round(avg_temp, 2) if avg_temp else 0
        }
    
    def get_recent_measurements(self, limit=10):
        """Get the most recent measurements"""
        results = self.session.query(ArgoData)\
            .order_by(ArgoData.timestamp.desc())\
            .limit(limit)\
            .all()
        
        # Convert to dictionary format
        return [{
            'float_id': r.float_id,
            'temperature': r.temperature,
            'salinity': r.salinity,
            'pressure': r.pressure,
            'latitude': r.latitude,
            'longitude': r.longitude,
            'timestamp': r.timestamp.isoformat() if r.timestamp else None
        } for r in results]
```

### Code Breakdown

**`__init__` method:**
```python
def __init__(self):
    self.session = get_session()
```
- **Constructor:** Runs when you create `DataService()` instance
- **self:** Refers to the object itself (like "me" in English)
- **get_session():** Opens a connection to the database
- **Why:** Need connection to query database

**`get_stats` method:**
```python
total_count = self.session.query(ArgoData).count()
```
- **query(ArgoData):** "I want to ask about ArgoData table"
- **.count():** "How many rows are there?"
- SQL equivalent: `SELECT COUNT(*) FROM argo_data;`

```python
unique_floats = self.session.query(
    func.count(func.distinct(ArgoData.float_id))
).scalar()
```
- **func.distinct():** Get unique values only
- **func.count():** Count them
- **scalar():** Return single value (not a list)
- SQL: `SELECT COUNT(DISTINCT float_id) FROM argo_data;`

**`get_recent_measurements` method:**
```python
results = self.session.query(ArgoData)\
    .order_by(ArgoData.timestamp.desc())\
    .limit(limit)\
    .all()
```
- **.order_by():** Sort results
- **.desc():** Descending (newest first)
- **.limit(limit):** Take only first N results
- **.all():** Execute query and return all matches
- SQL: `SELECT * FROM argo_data ORDER BY timestamp DESC LIMIT 10;`

**List comprehension:**
```python
return [{
    'float_id': r.float_id,
    'temperature': r.temperature,
    ...
} for r in results]
```
- **for r in results:** Loop through each result
- **{ ... }:** Create dictionary for each
- **Shorthand for:**
```python
output = []
for r in results:
    output.append({'float_id': r.float_id, ...})
return output
```

---

## 7. Frontend - React Application

### What is React?

React is a JavaScript library that makes building interactive UIs easy. Instead of manipulating HTML directly, you write **components** that automatically update when data changes.

### Key React Concepts

#### 1. Components
Think of components as LEGO blocks - reusable pieces that combine to make the full app.

#### 2. JSX (JavaScript XML)
Write HTML-like syntax in JavaScript:
```jsx
const greeting = <h1>Hello, World!</h1>;
```

#### 3. State
Data that can change over time. When state changes, React automatically re-renders the UI.

#### 4. Props
Data passed from parent to child components (like function parameters).

### Our Main Component (`frontend/src/App.jsx`)

```jsx
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // STATE: Data that changes over time
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  // EFFECT: Runs when component loads
  useEffect(() => {
    fetchStats();
  }, []); // Empty array = run once on mount

  // Fetch statistics from backend
  const fetchStats = async () => {
    try {
      const response = await fetch('/api/data/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  // Send message to AI
  const sendMessage = async () => {
    if (!input.trim()) return; // Don't send empty messages

    // Add user message to chat
    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput(''); // Clear input field
    setLoading(true);

    try {
      // Call backend API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();

      // Add AI response to chat
      const aiMessage = { sender: 'ai', text: data.response };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { 
        sender: 'ai', 
        text: 'Sorry, something went wrong.' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  // RENDER: What appears on screen
  return (
    <div className="App">
      <header>
        <h1>FloatChat-AI</h1>
        {stats && (
          <div className="stats">
            <p>Total Measurements: {stats.total_measurements}</p>
            <p>Unique Floats: {stats.unique_floats}</p>
            <p>Avg Temperature: {stats.average_temperature}°C</p>
          </div>
        )}
      </header>

      <div className="chat-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <strong>{msg.sender === 'user' ? 'You' : 'AI'}:</strong>
            <p>{msg.text}</p>
          </div>
        ))}
        {loading && <div className="loading">AI is thinking...</div>}
      </div>

      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask about ARGO data..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
```

### Code Explanation

**Imports:**
```jsx
import React, { useState, useEffect } from 'react';
```
- **useState:** Hook for managing state
- **useEffect:** Hook for side effects (like fetching data)

**State Declaration:**
```jsx
const [messages, setMessages] = useState([]);
```
- **messages:** Current value
- **setMessages:** Function to update value
- **useState([]):** Initial value is empty array
- **How it works:**
  - `messages` holds chat history
  - Call `setMessages(newValue)` to update
  - React automatically re-renders component

**useEffect Hook:**
```jsx
useEffect(() => {
  fetchStats();
}, []);
```
- **First argument:** Function to run
- **Second argument:** Dependency array
- **Empty array []:** Run only once (on component mount)
- **Use case:** Fetch initial data when page loads

**Async/Await Pattern:**
```jsx
const fetchStats = async () => {
  const response = await fetch('/api/data/stats');
  const data = await response.json();
  setStats(data);
};
```
- **async:** This function does asynchronous work
- **await:** Wait for this to complete before continuing
- **Why:** Network requests take time; don't block the UI
- **Alternative (old way):**
```jsx
fetch('/api/data/stats')
  .then(response => response.json())
  .then(data => setStats(data));
```

**Spread Operator:**
```jsx
setMessages(prev => [...prev, userMessage]);
```
- **prev:** Previous state value
- **...prev:** Spread (unpack) all previous messages
- **userMessage:** Add new message at end
- **Result:** New array with all old messages + new one
- **Why not `messages.push()`:** React needs a NEW array to detect changes

**Conditional Rendering:**
```jsx
{stats && (
  <div className="stats">
    <p>Total: {stats.total_measurements}</p>
  </div>
)}
```
- **stats &&:** If stats exists (not null/undefined), render this
- **Short-circuit evaluation:** If left side is false, right side doesn't run

**Map Function:**
```jsx
{messages.map((msg, index) => (
  <div key={index}>...</div>
))}
```
- **map():** Transform each array item into JSX
- **key={index}:** Unique identifier for each element (helps React optimize)
- **Equivalent to:**
```jsx
const elements = [];
for (let i = 0; i < messages.length; i++) {
  elements.push(<div key={i}>...</div>);
}
```

**Event Handlers:**
```jsx
onChange={(e) => setInput(e.target.value)}
```
- **onChange:** Event fired when input changes
- **e:** Event object
- **e.target:** The input element
- **e.target.value:** Current text in input
- **Result:** Updates state as user types

---

## 8. AI Integration - The Brain

### What is RAG (Retrieval-Augmented Generation)?

**Problem:** AI models don't know about your specific data
**Solution:** Give the AI relevant data before asking it to respond

**RAG Flow:**
1. User asks: "What's the latest temperature?"
2. **Retrieve:** Fetch relevant data from database
3. **Augment:** Add data to AI prompt as context
4. **Generate:** AI creates response based on data

### AI Service (`backend/services/ai_service.py`)

```python
import os
import requests
from dotenv import load_dotenv
from services.data_service import DataService

load_dotenv()

class AIService:
    def __init__(self):
        """Initialize AI service with configuration"""
        self.ai_mode = os.getenv('AI_MODE', 'ollama')
        self.data_service = DataService()
        
        if self.ai_mode == 'ollama':
            self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
            self.model = os.getenv('OLLAMA_MODEL', 'llama3.2')
        else:
            # OpenAI configuration
            import openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    def generate_response(self, user_query):
        """Main method: Generate AI response for user query"""
        # STEP 1: Retrieve relevant data (the "R" in RAG)
        context_data = self._get_context_data()
        
        # STEP 2: Build prompt with context (the "A" in RAG)
        prompt = self._build_prompt(user_query, context_data)
        
        # STEP 3: Call AI model (the "G" in RAG)
        if self.ai_mode == 'ollama':
            return self._call_ollama(prompt)
        else:
            return self._call_openai(prompt)
    
    def _get_context_data(self):
        """Retrieve relevant data from database"""
        stats = self.data_service.get_stats()
        recent = self.data_service.get_recent_measurements(limit=5)
        
        return {
            'statistics': stats,
            'recent_data': recent
        }
    
    def _build_prompt(self, user_query, context_data):
        """Construct detailed prompt with context"""
        prompt = f"""You are an expert oceanographic data assistant specializing in ARGO float data.

DATASET STATISTICS:
- Total Measurements: {context_data['statistics']['total_measurements']}
- Unique Floats: {context_data['statistics']['unique_floats']}
- Average Temperature: {context_data['statistics']['average_temperature']}°C

RECENT MEASUREMENTS:
"""
        for measurement in context_data['recent_data']:
            prompt += f"""
- Float {measurement['float_id']}:
  Temperature: {measurement['temperature']}°C
  Salinity: {measurement['salinity']} PSU
  Pressure: {measurement['pressure']} dbar
  Location: ({measurement['latitude']}, {measurement['longitude']})
  Time: {measurement['timestamp']}
"""
        
        prompt += f"\n\nUSER QUESTION: {user_query}\n\n"
        prompt += "Provide a clear, accurate answer based on the data above."
        
        return prompt
    
    def _call_ollama(self, prompt):
        """Call local Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Error: Ollama returned status {response.status_code}"
        
        except requests.exceptions.Timeout:
            return "The AI is taking too long to respond. Please try again."
        except Exception as e:
            return f"Error communicating with Ollama: {str(e)}"
    
    def _call_openai(self, prompt):
        """Call OpenAI API (alternative)"""
        import openai
        
        try:
            response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are an oceanographic data assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except openai.error.RateLimitError:
            return "OpenAI rate limit exceeded. Please try again later."
        except Exception as e:
            return f"Error with OpenAI: {str(e)}"
```

### Code Breakdown

**Environment Variables (.env file):**
```python
load_dotenv()
self.ai_mode = os.getenv('AI_MODE', 'ollama')
```
- **load_dotenv():** Loads variables from `.env` file
- **os.getenv():** Gets environment variable
- **Second argument:** Default value if not found
- **Why:** Keep secrets out of code (API keys, configurations)

**Dependency Injection:**
```python
self.data_service = DataService()
```
- Create instance of DataService
- Now we can call `self.data_service.get_stats()`
- **Pattern:** One service uses another service

**F-Strings (Formatted Strings):**
```python
prompt = f"Temperature: {temperature}°C"
```
- **f before quote:** Enables variable interpolation
- **{variable}:** Inserts variable value
- **Example:** If `temperature = 15.5`, output is "Temperature: 15.5°C"

**Try-Except Error Handling:**
```python
try:
    response = requests.post(...)
except requests.exceptions.Timeout:
    return "Timeout error"
except Exception as e:
    return f"General error: {str(e)}"
```
- **try:** Attempt this code
- **except:** If error occurs, run this instead
- **Multiple except:** Handle different error types differently
- **Why:** Prevent crashes; provide user-friendly error messages

**HTTP Request:**
```python
response = requests.post(
    f"{self.ollama_url}/api/generate",
    json={"model": self.model, "prompt": prompt},
    timeout=60
)
```
- **requests.post():** Send HTTP POST request
- **json=:** Body data (automatically converted to JSON)
- **timeout=60:** Wait max 60 seconds
- **Returns:** Response object with status_code, json(), text, etc.

---

## 9. Key Concepts & Patterns

### 1. REST API (Representational State Transfer)

**What:** Architecture style for web services
**How:** Uses HTTP methods (GET, POST, PUT, DELETE)

**Our API Endpoints:**
- `GET /api/data/stats` - Retrieve statistics
- `POST /api/chat` - Send message, get AI response

**Why REST:**
- Simple and widely understood
- Stateless (each request is independent)
- Cacheable responses

### 2. Separation of Concerns

**Principle:** Each part of code should have one job

**Our Structure:**
- **Models:** Define data structure
- **Services:** Business logic
- **Routes:** Handle HTTP requests
- **Frontend:** User interface

**Benefits:**
- Easy to test individual parts
- Changes in one area don't break others
- Multiple developers can work simultaneously

### 3. Environment Configuration

**File:** `.env`
```
FLASK_APP=app.py
FLASK_ENV=development
AI_MODE=ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

**Why:**
- Different settings for development vs. production
- Keep secrets out of code (API keys)
- Easy to change without modifying code

### 4. Virtual Environment

**What:** Isolated Python environment for each project
**Why:**
- Avoid dependency conflicts
- Each project has its own package versions
- Clean and reproducible setup

**Commands:**
```bash
# Create
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 5. Proxy Configuration

**File:** `frontend/package.json`
```json
"proxy": "http://localhost:5000"
```

**What it does:**
- Frontend (port 3000) talks to backend (port 5000)
- Requests to `/api/*` automatically forwarded to backend
- Avoids CORS (Cross-Origin Resource Sharing) issues

**Example:**
```jsx
fetch('/api/chat')  // Actually calls http://localhost:5000/api/chat
```

---

## 10. Code Walkthrough with Examples

### Example 1: Complete Request Flow

**Scenario:** User asks "What's the average temperature?"

#### Step 1: User types and clicks Send

**Frontend (App.jsx):**
```jsx
const sendMessage = async () => {
  const userMessage = { sender: 'user', text: input };
  setMessages([...messages, userMessage]); // Add to UI
  
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: input })
  });
  
  const data = await response.json();
  const aiMessage = { sender: 'ai', text: data.response };
  setMessages([...messages, userMessage, aiMessage]);
};
```

#### Step 2: Backend receives request

**Backend (app.py):**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Call AI service
    ai_service = AIService()
    response = ai_service.generate_response(user_message)
    
    return jsonify({'response': response})
```

#### Step 3: AI Service processes request

**AI Service (ai_service.py):**
```python
def generate_response(self, user_query):
    # Get data from database
    context_data = self._get_context_data()
    
    # Build prompt
    prompt = f"""
    Statistics: {context_data['statistics']}
    Recent data: {context_data['recent_data']}
    
    User question: {user_query}
    """
    
    # Call Ollama
    return self._call_ollama(prompt)
```

#### Step 4: Data Service queries database

**Data Service (data_service.py):**
```python
def get_stats(self):
    avg_temp = self.session.query(
        func.avg(ArgoData.temperature)
    ).scalar()
    
    return {'average_temperature': round(avg_temp, 2)}
```

#### Step 5: Response flows back

**Backend → Frontend:**
```json
{
  "response": "Based on the dataset, the average temperature is 15.42°C across all measurements."
}
```

**Frontend displays in chat.**

---

### Example 2: Database Query in Detail

**Task:** Get 5 most recent temperature readings above 20°C

```python
from db.models import ArgoData
from db.session import get_session

def get_warm_temperatures():
    session = get_session()
    
    results = session.query(ArgoData)\
        .filter(ArgoData.temperature > 20)\
        .order_by(ArgoData.timestamp.desc())\
        .limit(5)\
        .all()
    
    for record in results:
        print(f"Float {record.float_id}: {record.temperature}°C at {record.timestamp}")
```

**SQL Equivalent:**
```sql
SELECT * FROM argo_data
WHERE temperature > 20
ORDER BY timestamp DESC
LIMIT 5;
```

**Breakdown:**
1. `query(ArgoData)` - Select from argo_data table
2. `.filter(...)` - WHERE clause
3. `.order_by(...desc())` - ORDER BY ... DESC
4. `.limit(5)` - LIMIT 5
5. `.all()` - Execute and return all results

---

### Example 3: React State Management

**Scenario:** Toggle loading spinner

```jsx
function App() {
  const [loading, setLoading] = useState(false);
  
  const fetchData = async () => {
    setLoading(true);  // Show spinner
    
    try {
      const response = await fetch('/api/data');
      const data = await response.json();
      // Process data...
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);  // Hide spinner (runs whether success or error)
    }
  };
  
  return (
    <div>
      {loading && <div className="spinner">Loading...</div>}
      <button onClick={fetchData}>Fetch Data</button>
    </div>
  );
}
```

**Flow:**
1. User clicks button
2. `loading` becomes `true`
3. "Loading..." appears on screen
4. Data fetches
5. `loading` becomes `false`
6. "Loading..." disappears

---

## 11. How Everything Works Together

### Complete User Journey

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                         │
│  1. User types: "What's the warmest temperature recorded?"      │
│  2. Clicks "Send" button                                        │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                            │
│  3. sendMessage() function executes                             │
│  4. Adds user message to chat UI                                │
│  5. Sends POST request to /api/chat                             │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTP Request
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      BACKEND (Flask)                             │
│  6. app.py receives request at /api/chat route                  │
│  7. Extracts user message from JSON body                        │
│  8. Creates AIService instance                                   │
│  9. Calls ai_service.generate_response()                        │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      AI SERVICE                                  │
│  10. Calls data_service.get_stats()                             │
│  11. Calls data_service.get_recent_measurements()               │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      DATA SERVICE                                │
│  12. Queries database via SQLAlchemy                            │
│  13. Returns statistics and recent data                          │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      DATABASE (SQLite)                           │
│  14. Executes SQL queries                                       │
│  15. Returns raw data                                           │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      AI SERVICE (continued)                      │
│  16. Builds detailed prompt with retrieved data                 │
│  17. Sends prompt to Ollama API                                 │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      OLLAMA (LLM)                                │
│  18. Processes prompt with llama3.2 model                       │
│  19. Generates natural language response                        │
│  20. Returns: "The warmest temperature recorded was 28.5°C..."  │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      BACKEND (Flask)                             │
│  21. Receives AI response                                       │
│  22. Wraps in JSON: {"response": "The warmest..."}             │
│  23. Sends HTTP response to frontend                            │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                            │
│  24. Receives JSON response                                     │
│  25. Extracts response text                                     │
│  26. Adds AI message to chat UI                                 │
│  27. User sees answer on screen                                 │
└──────────────────────────────────────────────────────────────────┘
```

### Time Estimate for Each Step

- Steps 1-9: ~100ms (frontend + network)
- Steps 10-15: ~50ms (database query)
- Steps 16-20: ~5-20 seconds (AI generation)
- Steps 21-27: ~100ms (response handling)

**Total:** 5-20 seconds (AI is the bottleneck)

---

## 12. Common Viva Questions & Answers

### Basic Questions

**Q1: What is your project about?**
**A:** FloatChat-AI is an AI-powered conversational assistant for exploring oceanographic data. It allows users to ask questions in natural language and receive intelligent, data-backed answers about ARGO float measurements like temperature, salinity, and pressure.

**Q2: Why did you choose React for frontend?**
**A:** React provides component-based architecture, virtual DOM for efficient rendering, large community support, and excellent developer tools. It's perfect for building dynamic, responsive user interfaces.

**Q3: What is Flask?**
**A:** Flask is a lightweight Python web framework for building APIs and web applications. It's easy to learn, has minimal boilerplate, and integrates well with Python's data science ecosystem.

**Q4: Why SQLite instead of MySQL/PostgreSQL?**
**A:** SQLite is perfect for development and small-scale applications. It requires no server setup, stores everything in a single file, and is sufficient for our dataset size. For production with millions of records, we could migrate to PostgreSQL.

### Intermediate Questions

**Q5: Explain the three-tier architecture.**
**A:** 
- **Client Tier (Frontend):** React app handling UI and user interaction
- **Application Tier (Backend):** Flask server with business logic and APIs
- **Data Tier (Database):** SQLite storing ARGO float measurements

This separation provides modularity, scalability, and maintainability.

**Q6: What is an ORM? Why use SQLAlchemy?**
**A:** ORM (Object-Relational Mapper) bridges object-oriented programming and relational databases. Instead of writing SQL, we write Python. Benefits include:
- Type safety and autocomplete
- Database-agnostic code
- Automatic query optimization
- Prevention of SQL injection attacks

**Q7: What is RAG?**
**A:** Retrieval-Augmented Generation. It's a pattern where:
1. **Retrieve:** Fetch relevant data from database
2. **Augment:** Add data to AI prompt as context
3. **Generate:** AI produces response based on actual data

This grounds AI responses in facts rather than hallucinations.

**Q8: Why Ollama instead of OpenAI?**
**A:** 
- **Cost:** Ollama is free; OpenAI charges per token
- **Privacy:** Data stays on local machine
- **Control:** No rate limits or quota issues
- **Learning:** Better for academic projects

We initially used OpenAI but pivoted due to quota limits.

### Advanced Questions

**Q9: Explain the service layer pattern.**
**A:** Instead of putting all logic in route handlers, we create service classes:
- `DataService`: Handles database operations
- `AIService`: Manages AI interactions

**Benefits:**
- Reusability (services can be used by multiple routes)
- Testability (test services independently)
- Separation of concerns (each service has one responsibility)

**Q10: How does React's state management work?**
**A:** React uses hooks like `useState`:
```jsx
const [count, setCount] = useState(0);
```
- `count`: Current value
- `setCount`: Function to update value
- When state updates, React re-renders the component

This creates reactive UI - changes in data automatically update the display.

**Q11: Explain async/await.**
**A:** Modern way to handle asynchronous operations:
```python
async def fetch_data():
    response = await requests.get(url)
    return response.json()
```
- `async`: Declares asynchronous function
- `await`: Pauses execution until operation completes
- **Benefit:** Cleaner than callbacks/promises; looks like synchronous code

**Q12: How do you prevent SQL injection?**
**A:** SQLAlchemy automatically parameterizes queries:
```python
# Safe (parameterized)
session.query(ArgoData).filter(ArgoData.float_id == user_input)

# Unsafe (string concatenation)
session.execute(f"SELECT * FROM argo_data WHERE float_id = '{user_input}'")
```

**Q13: What is CORS? How did you handle it?**
**A:** Cross-Origin Resource Sharing. Browsers block requests from one domain to another for security. We solved this with proxy configuration in `package.json`:
```json
"proxy": "http://localhost:5000"
```
Frontend requests to `/api/*` are automatically forwarded to backend.

**Q14: How would you scale this application?**
**A:**
1. **Database:** Migrate from SQLite to PostgreSQL with connection pooling
2. **Backend:** Use Gunicorn/uWSGI with multiple workers
3. **Frontend:** Deploy to CDN (Cloudflare, Netlify)
4. **Caching:** Add Redis for frequent queries
5. **Load Balancer:** Distribute traffic across multiple backend servers
6. **AI:** Queue system for LLM requests (Celery + RabbitMQ)

**Q15: What security measures did you implement?**
**A:**
1. **Environment Variables:** Secrets in `.env`, not in code
2. **SQLAlchemy ORM:** Prevents SQL injection
3. **Input Validation:** Check user input before processing
4. **HTTPS:** (Would add in production)
5. **Rate Limiting:** (Would add to prevent abuse)

### Troubleshooting Questions

**Q16: What challenges did you face?**
**A:**
1. **Network Errors:** Argovis API was inaccessible
   - **Solution:** Created synthetic data generator
2. **OpenAI Quota:** Exceeded free tier limits
   - **Solution:** Pivoted to Ollama (local AI)
3. **Ollama Timeouts:** Model took too long to respond
   - **Solution:** Increased timeout, simplified prompts, pre-warmed model

**Q17: How do you debug issues?**
**A:**
1. **Logging:** Add print statements and structured logging
2. **Browser DevTools:** Check network requests, console errors
3. **Python Debugger:** Use `pdb` for step-through debugging
4. **Test in Isolation:** Test each component separately
5. **Read Error Messages:** Stack traces provide valuable clues

---

## 13. Troubleshooting Guide

### Common Issues & Solutions

#### Issue 1: Backend won't start

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Cause:** Virtual environment not activated or dependencies not installed

**Solution:**
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

#### Issue 2: Frontend can't connect to backend

**Error:** `Failed to fetch` or `Network Error`

**Cause:** Backend not running or proxy misconfigured

**Solution:**
1. Ensure backend is running on port 5000
2. Check `package.json` has `"proxy": "http://localhost:5000"`
3. Restart frontend: `npm start`

#### Issue 3: Database empty

**Error:** `No data found` or statistics show zeros

**Solution:**
```bash
cd backend
python generate_sample_data.py
```

#### Issue 4: Ollama timeout

**Error:** `Read timed out` or `Connection timeout`

**Cause:** Ollama not running or model not pulled

**Solution:**
```bash
# Start Ollama
ollama serve

# Pull model (in new terminal)
ollama pull llama3.2

# Test
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Hello"
}'
```

#### Issue 5: React errors

**Error:** `Cannot read property 'map' of undefined`

**Cause:** State not initialized properly

**Solution:** Always initialize state with correct type:
```jsx
const [messages, setMessages] = useState([]);  // Empty array, not null
```

---

## Key Takeaways for Viva

### What You Built
1. **Full-stack web application** with React + Flask
2. **AI-powered chat interface** using Ollama
3. **RAG system** that grounds AI in real data
4. **RESTful API** with proper architecture

### Technologies Mastered
1. **Frontend:** React, JSX, Hooks, async/await
2. **Backend:** Flask, SQLAlchemy, REST APIs
3. **Database:** SQLite, ORM, SQL queries
4. **AI:** Ollama, prompt engineering, RAG pattern
5. **Tools:** Git, pip, npm, virtual environments

### Software Engineering Practices
1. **Architecture:** Three-tier, separation of concerns
2. **Design Patterns:** Service layer, MVC
3. **Best Practices:** Environment config, error handling
4. **Testing:** Manual testing, debugging strategies

### Problem-Solving Skills
1. Pivoted from OpenAI to Ollama when blocked
2. Created synthetic data when API unavailable
3. Optimized Ollama integration for performance
4. Documented everything for future maintenance

---

## Final Tips for Viva

1. **Understand the Flow:** Be able to trace a request from user click to AI response
2. **Know Your Code:** Explain any line someone points to
3. **Admit Limitations:** "This could be improved by..." shows maturity
4. **Connect to Theory:** Link project to course concepts (databases, networks, AI)
5. **Be Honest:** If you don't know, say so and describe how you'd find out
6. **Show Enthusiasm:** You built something cool - be proud!

---

**Good luck with your viva! You've built an impressive project. 🚀**
