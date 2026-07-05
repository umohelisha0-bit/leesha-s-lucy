# Leesha's Lucy - Complete AI Video Call System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

🎬 Advanced full-body AI video call system with unlimited sessions, no time restrictions, and no watermarks.

## ✨ Key Features

- 📹 **Real-time HD Video Calling** - WebRTC-based communication
- 🤖 **AI-Powered Conversations** - GPT-4 integration for natural dialogue
- 🎤 **Advanced Speech Recognition** - OpenAI Whisper for accurate transcription
- 🔊 **Natural Text-to-Speech** - ElevenLabs integration for realistic audio
- 😊 **Emotion Detection** - Real-time facial, voice, and text emotion analysis
- 👤 **Realistic 3D Avatar** - Full-body animations with natural expressions
- ⚡ **Ultra Low Latency** - Optimized WebSocket communication
- 📊 **Comprehensive Analytics** - Full call tracking and statistics
- ♾️ **Unlimited Duration** - No session timeouts or time limits
- 🎨 **No Watermarks** - Fully customizable branding

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)
- PostgreSQL 12+ (or use Docker)
- Redis 6+ (or use Docker)

### Installation with Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/umohelisha0-bit/leesha-s-lucy.git
cd leesha-s-lucy

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# - OPENAI_API_KEY
# - ELEVENLABS_API_KEY

# Start all services
docker-compose up --build
```

Application will be available at:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### Manual Installation

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000" > .env
echo "REACT_APP_WS_URL=ws://localhost:8000" >> .env

# Start development server
npm start
```

## 📚 Project Structure

```
leesha-s-lucy/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # Database setup
│   │   ├── api/
│   │   │   ├── calls.py            # Call endpoints
│   │   │   ├── ai.py               # AI service endpoints
│   │   │   └── analytics.py        # Analytics endpoints
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── call.py
│   │   │   ├── message.py
│   │   │   └── emotion.py
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   ├── speech_service.py
│   │   │   ├── avatar_service.py
│   │   │   └── emotion_service.py
│   │   └── ws/
│   │       ├── manager.py          # WebSocket connection management
│   │       └── handlers.py         # WebSocket message handlers
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── index.js
│   │   ├── App.js
│   │   ├── pages/
│   │   │   ├── LandingPage.js      # Home page
│   │   │   ├── VideoCall.js        # Call interface
│   │   │   └── History.js          # Call history
│   │   ├── components/
│   │   │   └── AvatarDisplay.js    # Avatar component
│   │   └── services/
│   │       ├── apiService.js       # API client
│   │       └── websocketService.js # WebSocket client
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
│
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔌 API Documentation

### REST Endpoints

#### Call Management
```
POST   /api/calls/start              # Start new call
GET    /api/calls/{call_id}          # Get call details
POST   /api/calls/{call_id}/end      # End call
GET    /api/calls/{call_id}/sessions # Get sessions
```

#### AI Services
```
POST   /api/ai/chat                          # Chat with AI
POST   /api/ai/voice/transcribe              # Transcribe audio
POST   /api/ai/voice/synthesize              # Synthesize speech
GET    /api/ai/avatar/init                   # Initialize avatar
POST   /api/ai/avatar/update-state           # Update avatar state
POST   /api/ai/avatar/gesture                # Animate gesture
POST   /api/ai/emotion/detect-face           # Detect face emotion
POST   /api/ai/emotion/detect-voice          # Detect voice emotion
POST   /api/ai/emotion/detect-text           # Analyze text emotion
```

#### Analytics
```
GET    /api/analytics/calls                  # Call history
GET    /api/analytics/stats                  # Usage statistics
GET    /api/analytics/messages/{call_id}     # Get call messages
```

### WebSocket

**Endpoint:** `WS /ws/call/{call_id}/{connection_id}`

**Message Types:**
```json
// Chat message
{
  "type": "chat",
  "content": "Hello",
  "emotion_context": {"emotion": "happy"},
  "history": []
}

// Voice message
{
  "type": "voice",
  "audio_data": "base64_encoded_audio"
}

// Emotion detection
{
  "type": "emotion",
  "emotion_type": "face", // or "voice", "text"
  "data": "base64_or_text"
}

// Avatar request
{
  "type": "avatar_request",
  "request_type": "update",
  "emotion": "happy",
  "action": "talk"
}

// Heartbeat
{
  "type": "heartbeat"
}
```

## ⚙️ Configuration

All configuration through `.env` file. See `.env.example` for all options.

**Key Settings:**
```bash
# API Keys
OPENAI_API_KEY=sk-xxx
ELEVENLABS_API_KEY=xxx

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/lucy_ai
REDIS_URL=redis://localhost:6379

# Features (Set to None for unlimited)
SESSION_TIMEOUT=None              # No timeout
SESSION_MAX_DURATION=None         # Unlimited duration
```

## 🔧 Technology Stack

**Backend:**
- FastAPI (async web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- PostgreSQL (database)
- Redis (caching)
- WebSockets (real-time)

**AI/ML:**
- OpenAI GPT-4 (language model)
- Whisper (speech recognition)
- ElevenLabs (text-to-speech)
- MediaPipe (emotion detection)
- Librosa (audio processing)

**Frontend:**
- React 18
- Material-UI
- Socket.io (WebSocket)
- Three.js (3D rendering)
- Axios (HTTP client)

**DevOps:**
- Docker & Docker Compose
- PostgreSQL
- Redis
- Nginx

## 📊 Performance

- Real-time WebSocket communication
- Async/await for non-blocking I/O
- Connection pooling
- Redis caching
- GPU acceleration support
- Optimized for low latency (<100ms)

## 🚀 Deployment

### Docker Compose (Recommended)

```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Cloud Deployment

- **AWS**: EC2 + RDS + ElastiCache
- **Google Cloud**: Cloud Run + Cloud SQL + Memorystore
- **Azure**: App Service + Database + Cache for Redis

## 📝 Environment Variables

```bash
# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/lucy_ai

# AI Services
OPENAI_API_KEY=sk-your-key
ELEVENLABS_API_KEY=your-key

# Features
SESSION_TIMEOUT=None               # No timeout = unlimited
SESSION_MAX_DURATION=None          # No limit = unlimited

# Logging
LOG_LEVEL=INFO
```

## 🔐 Security

**Note:** This system has NO authentication/security built-in (as per requirements for unlimited access). For production, add:

- JWT authentication
- HTTPS/WSS encryption
- Rate limiting
- Input validation
- SQL injection prevention (already using SQLAlchemy ORM)

## 📈 Monitoring

- Health check endpoint: `GET /health`
- Structured logging
- Performance metrics
- Error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙋 Support

For issues and questions:
- Open a GitHub issue
- Check existing documentation
- Review API docs at `/docs`

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Multi-party group calls
- [ ] Screen sharing
- [ ] Recording & playback
- [ ] Real-time translation
- [ ] Custom avatar training
- [ ] Voice cloning
- [ ] Advanced analytics dashboard

## 🎉 Credits

Built with ❤️ by Leesha

**Core Libraries:**
- FastAPI
- React
- OpenAI
- ElevenLabs
- MediaPipe

---

**Made with ❤️ for unlimited AI video conversations**
