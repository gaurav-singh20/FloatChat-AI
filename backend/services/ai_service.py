"""
AI Service Module
Handles AI-powered chat responses using OpenAI API or Ollama with ARGO data context
"""
import os
from typing import Dict, Any, List
import json
from dotenv import load_dotenv

load_dotenv()

# Check if OpenAI is available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI library not installed. Install with: pip install openai")

# Check if requests is available for Ollama
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class AIService:
    """Service for generating AI responses with oceanographic context"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY', '')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.ai_mode = os.getenv('AI_MODE', 'openai').lower()  # 'openai' or 'ollama'
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
        
        self.use_ai = False
        self.client = None
        
        # Try Ollama first if specified
        if self.ai_mode == 'ollama' and REQUESTS_AVAILABLE:
            if self._test_ollama():
                self.use_ai = True
                print(f"✅ Ollama connected successfully")
                print(f"🤖 Using local model: {self.ollama_model}")
                print(f"🔗 Ollama URL: {self.ollama_url}")
            else:
                print("⚠️ Ollama not available, falling back to OpenAI or fallback mode")
                self.ai_mode = 'openai'
        
        # Try OpenAI if Ollama not used or failed
        if self.ai_mode == 'openai' and not self.use_ai:
            if OPENAI_AVAILABLE and self.api_key and not self.api_key.startswith('your_'):
                try:
                    self.client = OpenAI(api_key=self.api_key)
                    self.use_ai = True
                    print(f"✅ OpenAI client initialized successfully")
                    print(f"🤖 Model: {self.model}")
                    print(f"🔑 API Key configured (starts with: {self.api_key[:7]}...)")
                except Exception as e:
                    print(f"❌ Failed to initialize OpenAI: {e}")
                    self.use_ai = False
            else:
                if not self.api_key:
                    print("⚠️ OPENAI_API_KEY not set in .env file")
                elif self.api_key.startswith('your_'):
                    print("⚠️ OPENAI_API_KEY is still placeholder")
                elif not OPENAI_AVAILABLE:
                    print("⚠️ OpenAI library not available")
        
        if not self.use_ai:
            print("💡 TIP: Install Ollama for free local AI: https://ollama.ai")
            print("   Or add OpenAI credits at: https://platform.openai.com/billing")
        
        self.system_prompt = self._build_system_prompt()
    
    def _test_ollama(self) -> bool:
        """Test if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for the AI assistant"""
        return """You are FloatChat, an expert oceanographic AI assistant specializing in ARGO float data analysis.

ARGO floats are autonomous profiling instruments that drift with ocean currents and measure:
- Temperature (°C)
- Salinity (PSU - Practical Salinity Units)
- Pressure/Depth (dbar - decibars)
- Geographic position (latitude/longitude)

Your role:
1. Answer questions about oceanographic data from ARGO floats
2. Interpret temperature, salinity, and depth measurements
3. Explain ocean phenomena and patterns
4. Provide insights based on the provided data context
5. Be conversational yet scientific and accurate

When provided with data context:
- Reference specific measurements and statistics
- Explain trends and patterns you observe
- Compare values to typical ocean conditions
- Mention the float ID and location when relevant

If insufficient data is available, explain what data would be needed to answer properly.

Always be helpful, clear, and scientifically accurate. Use appropriate units and explain technical terms."""
    
    def generate_response(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """
        Generate AI response based on user message and data context
        
        Args:
            user_message: The user's question or message
            context_data: Dictionary containing relevant ARGO data and statistics
        
        Returns:
            AI-generated response string
        """
        if not self.use_ai:
            print("⚠️ AI not available, using fallback response")
            return self._generate_fallback_response(user_message, context_data)
        
        try:
            # Format context for the AI
            context_str = self._format_context(context_data)
            
            if self.ai_mode == 'ollama':
                return self._call_ollama(user_message, context_str)
            else:
                return self._call_openai(user_message, context_str)
        
        except Exception as e:
            print(f"❌ Error generating AI response: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            return self._generate_fallback_response(user_message, context_data)
    
    def _call_openai(self, user_message: str, context_str: str) -> str:
        """Call OpenAI API"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""User Question: {user_message}

Available Data Context:
{context_str}

Please provide a helpful, accurate response based on this data."""}
        ]
        
        print(f"🤖 Calling OpenAI API with model: {self.model}")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        
        ai_response = response.choices[0].message.content.strip()
        print(f"✅ OpenAI response received ({len(ai_response)} chars)")
        return ai_response
    
    def _call_ollama(self, user_message: str, context_str: str) -> str:
        """Call Ollama local API with streaming for faster response"""
        # Simplified prompt for faster processing
        prompt = f"""You are FloatChat, an oceanographic AI assistant analyzing ARGO float data.

Data Summary: {context_str[:800]}

Question: {user_message}

Provide a clear, concise answer (2-3 paragraphs) based on the data."""
        
        print(f"🤖 Calling Ollama with model: {self.ollama_model}")
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 500,  # Reduced for faster response
                        "top_k": 40,
                        "top_p": 0.9
                    }
                },
                timeout=120  # Increased timeout
            )
            
            if response.status_code == 200:
                ai_response = response.json().get('response', '').strip()
                print(f"✅ Ollama response received ({len(ai_response)} chars)")
                return ai_response
            else:
                raise Exception(f"Ollama error: {response.status_code}")
        except requests.exceptions.Timeout:
            print("⚠️ Ollama timed out - the model might be loading for the first time")
            return "I'm warming up! This is your first query and the AI model is loading. Please try asking your question again in a few seconds. Subsequent responses will be much faster! 🚀"
    
    def _format_context(self, context_data: Dict[str, Any]) -> str:
        """Format context data into a readable string for the AI"""
        parts = []
        
        # Add dataset statistics
        if 'stats' in context_data:
            stats = context_data['stats']
            
            if stats.get('total_records', 0) == 0:
                return "No ARGO data is currently available in the database. Please ingest data first."
            
            parts.append("=== ARGO Dataset Overview ===")
            parts.append(f"Total Records: {stats.get('total_records', 0):,}")
            parts.append(f"Float IDs: {', '.join(stats.get('floats', []))}")
            
            if 'date_range' in stats:
                dr = stats['date_range']
                parts.append(f"Date Range: {dr.get('min', 'N/A')} to {dr.get('max', 'N/A')}")
            
            if 'depth_range' in stats:
                dp = stats['depth_range']
                parts.append(f"Depth Range: {dp.get('min', 'N/A')} - {dp.get('max', 'N/A')} {dp.get('unit', 'dbar')}")
            
            if 'temperature' in stats:
                temp = stats['temperature']
                parts.append(f"Temperature Range: {temp.get('min', 'N/A')} - {temp.get('max', 'N/A')} {temp.get('unit', '°C')}")
                parts.append(f"Average Temperature: {temp.get('avg', 'N/A')} {temp.get('unit', '°C')}")
            
            if 'salinity' in stats:
                sal = stats['salinity']
                parts.append(f"Salinity Range: {sal.get('min', 'N/A')} - {sal.get('max', 'N/A')} {sal.get('unit', 'PSU')}")
                parts.append(f"Average Salinity: {sal.get('avg', 'N/A')} {sal.get('unit', 'PSU')}")
            
            if 'geographic_bounds' in stats:
                geo = stats['geographic_bounds']
                lat = geo.get('latitude', {})
                lon = geo.get('longitude', {})
                parts.append(f"Geographic Area: Lat {lat.get('min', 'N/A')}° to {lat.get('max', 'N/A')}°, Lon {lon.get('min', 'N/A')}° to {lon.get('max', 'N/A')}°")
        
        # Add sample data if available
        if 'sample_data' in context_data and context_data['sample_data']:
            parts.append("\n=== Sample Measurements ===")
            samples = context_data['sample_data'][:10]  # Limit to 10 samples
            
            for i, sample in enumerate(samples, 1):
                parts.append(f"\nMeasurement {i}:")
                parts.append(f"  Time: {sample.get('time', 'N/A')}")
                parts.append(f"  Position: {sample.get('latitude', 'N/A')}°N, {sample.get('longitude', 'N/A')}°E")
                parts.append(f"  Depth: {sample.get('depth', 'N/A')} dbar")
                parts.append(f"  Temperature: {sample.get('temperature', 'N/A')} °C")
                parts.append(f"  Salinity: {sample.get('salinity', 'N/A')} PSU")
        
        return "\n".join(parts)
    
    def _generate_fallback_response(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """
        Generate a rule-based response when AI is not available
        
        This provides basic responses without OpenAI API
        """
        stats = context_data.get('stats', {})
        
        # Check if data exists
        if stats.get('total_records', 0) == 0:
            return """I don't have any ARGO data loaded yet. To get started:

1. Make sure you have internet connection
2. Run: python fetch_argovis.py
3. This will download oceanographic data from ARGO floats

Once data is loaded, I'll be able to answer questions about ocean temperature, salinity, and depth measurements!"""
        
        # Basic query understanding
        query_lower = user_message.lower()
        
        # Temperature queries
        if any(word in query_lower for word in ['temperature', 'temp', 'warm', 'cold', 'hot']):
            temp = stats.get('temperature', {})
            return f"""Based on the ARGO float data:

**Temperature Statistics:**
- Range: {temp.get('min', 'N/A')} to {temp.get('max', 'N/A')} {temp.get('unit', '°C')}
- Average: {temp.get('avg', 'N/A')} {temp.get('unit', '°C')}

The dataset contains {stats.get('total_records', 0):,} measurements from {stats.get('float_count', 0)} float(s) in the Indian Ocean region.

Note: For more detailed analysis, please set up your OPENAI_API_KEY in the .env file."""
        
        # Salinity queries
        if any(word in query_lower for word in ['salinity', 'salt', 'saline']):
            sal = stats.get('salinity', {})
            return f"""Based on the ARGO float data:

**Salinity Statistics:**
- Range: {sal.get('min', 'N/A')} to {sal.get('max', 'N/A')} {sal.get('unit', 'PSU')}
- Average: {sal.get('avg', 'N/A')} {sal.get('unit', 'PSU')}

PSU (Practical Salinity Units) is the standard measure of ocean salinity. Typical ocean salinity is around 35 PSU.

Note: For more detailed analysis, please set up your OPENAI_API_KEY in the .env file."""
        
        # Depth queries
        if any(word in query_lower for word in ['depth', 'deep', 'shallow', 'surface']):
            depth = stats.get('depth_range', {})
            return f"""Based on the ARGO float data:

**Depth Coverage:**
- Range: {depth.get('min', 'N/A')} to {depth.get('max', 'N/A')} {depth.get('unit', 'dbar')}

ARGO floats typically profile from the surface down to 2000 meters, collecting data at various depths as they ascend.

Note: For more detailed analysis, please set up your OPENAI_API_KEY in the .env file."""
        
        # General info queries
        if any(word in query_lower for word in ['info', 'overview', 'summary', 'what', 'tell', 'about']):
            floats = ', '.join(stats.get('floats', []))
            date_range = stats.get('date_range', {})
            
            return f"""**FloatChat ARGO Data Overview** 🌊

I have access to {stats.get('total_records', 0):,} oceanographic measurements from the Indian Ocean region.

**Dataset Details:**
- Float ID(s): {floats}
- Date Range: {date_range.get('min', 'N/A')} to {date_range.get('max', 'N/A')}
- Measurements: Temperature, Salinity, Depth, Position

**What I can help with:**
- Ocean temperature patterns
- Salinity variations
- Depth profiles
- Geographic analysis
- Data trends and statistics

Try asking me about temperature, salinity, or depth characteristics!

Note: For AI-powered insights, please add your OPENAI_API_KEY to the .env file."""
        
        # Default response
        return f"""I'm FloatChat, your ARGO oceanographic data assistant! 🌊

I have {stats.get('total_records', 0):,} measurements available from {stats.get('float_count', 0)} float(s).

**You can ask me about:**
- Temperature statistics and ranges
- Salinity measurements
- Depth profiles
- Geographic coverage
- Data overview and summaries

**Note:** AI-powered responses are currently unavailable. To enable full conversational AI:
1. Get an OpenAI API key from https://platform.openai.com
2. Add it to your .env file as OPENAI_API_KEY=your_key_here
3. Restart the server

I can still provide basic data analysis without AI!"""
