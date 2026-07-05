# Leesha's Lucy - Complete Backend Setup

## Installation

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Redis 6+

### Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run migrations:**
```bash
alembic upgrade head
```

5. **Start server:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation

Swagger UI: `http://localhost:8000/docs`

## Key Features

✅ **Unlimited Duration** - No session timeouts or time restrictions
✅ **No Watermarks** - Full control over branding
✅ **AI Conversations** - GPT-4 powered responses
✅ **Emotion Detection** - Real-time emotion analysis
✅ **Avatar System** - 3D avatar with animations
✅ **Real-time Communication** - WebSocket-based
✅ **Analytics** - Full call tracking and statistics

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration management
│   ├── database.py       # Database setup
│   ├── api/              # API endpoints
│   │   ├── calls.py      # Call management
│   │   ├── ai.py         # AI services
│   │   └── analytics.py  # Analytics
│   ├── models/           # Database models
│   │   ├── call.py
│   │   ├── user.py
│   │   ├── message.py
│   │   └── emotion.py
│   ├── services/         # Business logic
│   │   ├── ai_service.py
│   │   ├── speech_service.py
│   │   ├── avatar_service.py
│   │   └── emotion_service.py
│   └── ws/               # WebSocket handlers
│       ├── manager.py
│       └── handlers.py
├── requirements.txt
├── Dockerfile
└── .env.example
```

## Deployment

### Docker
```bash
docker build -t lucy-backend .
docker run -p 8000:8000 lucy-backend
```

### Docker Compose
```bash
docker-compose up -d
```

## Configuration

All configuration is managed through environment variables. See `.env.example`.

## API Endpoints

### Calls
- `POST /api/calls/start` - Start new call
- `GET /api/calls/{call_id}` - Get call details
- `POST /api/calls/{call_id}/end` - End call
- `GET /api/calls/{call_id}/sessions` - Get sessions

### AI Services
- `POST /api/ai/chat` - Chat with AI
- `POST /api/ai/voice/transcribe` - Transcribe audio
- `POST /api/ai/voice/synthesize` - Synthesize speech
- `GET /api/ai/avatar/init` - Initialize avatar
- `POST /api/ai/emotion/*` - Detect emotion

### Analytics
- `GET /api/analytics/calls` - Call history
- `GET /api/analytics/stats` - Statistics
- `GET /api/analytics/messages/{call_id}` - Get messages

## WebSocket

`WS /ws/call/{call_id}/{connection_id}`

Message types:
- `chat` - Text message
- `voice` - Audio message
- `emotion` - Emotion detection
- `avatar_request` - Avatar control
- `heartbeat` - Keep-alive

## License

MIT
