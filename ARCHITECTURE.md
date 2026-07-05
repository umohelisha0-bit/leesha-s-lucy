# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Browser)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            React 18 Frontend Application             │  │
│  │  ┌──────────────┐  ┌──────────────────────────────┐  │  │
│  │  │ Landing Page │  │  Video Call Interface        │  │  │
│  │  ├──────────────┤  ├──────────────────────────────┤  │  │
│  │  │ Start Call   │  │ - Avatar Display             │  │  │
│  │  │ View History │  │ - Chat Messages              │  │  │
│  │  │ Analytics    │  │ - Voice Input/Output         │  │  │
│  │  └──────────────┘  │ - Emotion Feedback           │  │  │
│  │                    └──────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │        API Service + WebSocket Client          │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                                          │
         │ REST API (Axios)                        │ WebSocket (Socket.io)
         │                                          │
┌────────▼──────────────────────────────────────────▼────────┐
│                  FastAPI Backend (Python)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Endpoint Router                     │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │ /api/calls         │ /api/ai          │ /api/...    │  │
│  │ - Start call       │ - Chat           │             │  │
│  │ - End call         │ - Voice synthesis│ /api/...    │  │
│  │ - Get call details │ - Voice transcribe           │  │
│  │ - Get sessions     │ - Avatar control │             │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         WebSocket Connection Manager               │  │
│  │    /ws/call/{call_id}/{connection_id}              │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │ - Connection pooling                                │  │
│  │ - Message routing                                   │  │
│  │ - Broadcast handling                                │  │
│  │ - Heartbeat management                              │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Service Layer (Business Logic)         │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │ ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │  │
│  │ │   AI        │  │  Speech     │  │  Avatar    │  │  │
│  │ │  Service    │  │  Service    │  │  Service   │  │  │
│  │ │             │  │             │  │            │  │  │
│  │ │ - ChatGPT   │  │ - Whisper   │  │ - Gestures │  │  │
│  │ │ - Context   │  │ - ElevenLabs│  │ - Emotions │  │  │
│  │ │   mgmt      │  │ - Audio ops │  │ - Lip-sync │  │  │
│  │ └─────────────┘  └─────────────┘  └────────────┘  │  │
│  │                                                      │  │
│  │ ┌──────────────────────┐  ┌──────────────────────┐ │  │
│  │ │   Emotion Service    │  │   Analytics Service  │ │  │
│  │ │                      │  │                      │ │  │
│  │ │ - Face detection     │  │ - Call tracking      │ │  │
│  │ │ - Voice analysis     │  │ - Statistics         │ │  │
│  │ │ - Text sentiment     │  │ - History storage    │ │  │
│  │ └──────────────────────┘  └──────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Data Layer (Database & Cache)               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
         │                          │
         │ SQLAlchemy ORM          │ Redis Client
         │                          │
┌────────▼──────────────┐  ┌───────▼──────────────┐
│  PostgreSQL Database  │  │   Redis Cache        │
│                       │  │                      │
│ Tables:               │  │ - Session data       │
│ - users               │  │ - Connection cache   │
│ - calls               │  │ - Rate limiting      │
│ - messages            │  │ - Temporary storage  │
│ - emotions            │  │                      │
│ - call_sessions       │  │                      │
└───────────────────────┘  └──────────────────────┘
```

## Data Flow

### Chat Message Flow

```
1. User sends message
   ↓
2. WebSocket receives message
   ↓
3. Message Handler processes
   ↓
4. AI Service generates response
   ↓
5. Emotion Service detects user emotion
   ↓
6. Avatar Service creates animations
   ↓
7. Speech Service synthesizes audio
   ↓
8. Message broadcast to all connections
   ↓
9. Store in database
   ↓
10. Update analytics
```

### Voice Message Flow

```
1. User records audio
   ↓
2. Send via WebSocket
   ↓
3. Speech Service transcribes (Whisper)
   ↓
4. Emotion Service analyzes voice
   ↓
5. AI Service generates response
   ↓
6. Speech Service synthesizes reply
   ↓
7. Send audio + text response
   ↓
8. Avatar animates and speaks
   ↓
9. Store conversation in database
```

## Technology Stack

### Backend
- **Framework**: FastAPI (async Python web framework)
- **Server**: Uvicorn (ASGI server)
- **ORM**: SQLAlchemy (database abstraction)
- **Database**: PostgreSQL (relational database)
- **Cache**: Redis (in-memory cache)
- **WebSocket**: python-socketio
- **AI**: OpenAI API (GPT-4)
- **TTS**: ElevenLabs API
- **STT**: OpenAI Whisper
- **Emotion**: MediaPipe, librosa
- **Audio**: PyAudio, scipy
- **Video**: OpenCV

### Frontend
- **Framework**: React 18 (UI library)
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **WebSocket**: socket.io-client
- **UI Components**: Material-UI (MUI)
- **3D Graphics**: Three.js
- **State Management**: Zustand
- **Styling**: CSS-in-JS (Emotion)

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Reverse Proxy**: Nginx
- **SSL/TLS**: Let's Encrypt
- **CI/CD**: GitHub Actions (ready for setup)

## Scalability

### Horizontal Scaling

```
┌─────────────────────────────────────┐
│     Load Balancer (Nginx)           │
└──────────────┬──────────────────────┘
               │
       ┌───────┼───────┐
       │       │       │
   ┌───▼──┐ ┌─▼───┐ ┌─▼───┐
   │ API  │ │ API │ │ API │
   │ #1   │ │ #2  │ │ #3  │
   └───┬──┘ └─┬───┘ └─┬───┘
       │       │       │
       └───────┼───────┘
               │
        ┌──────▼──────┐
        │ PostgreSQL  │
        │ (Replicated)│
        └─────────────┘
        
        ┌─────────────┐
        │ Redis Cluster
        │ (3+ nodes)  │
        └─────────────┘
```

### Performance Optimization

1. **Database**
   - Connection pooling (20 connections, 40 overflow)
   - Query caching via Redis
   - Indexed columns for fast lookups

2. **WebSocket**
   - Message compression
   - Binary protocol support
   - Heartbeat/keepalive

3. **API**
   - Async/await (non-blocking I/O)
   - Response caching
   - Gzip compression

4. **Frontend**
   - Code splitting
   - Lazy loading
   - Image optimization
   - Service workers

## Security Architecture

⚠️ **Current Status**: NO authentication/security (as per requirements)

**For Production, Add:**

```
┌──────────────────────────────────────┐
│  API Gateway (Authentication)        │
│  - JWT token validation              │
│  - Rate limiting                     │
│  - Request validation                │
└──────────────┬───────────────────────┘
               │
        ┌──────▼──────────┐
        │ Authenticated   │
        │ Request         │
        │ Processing      │
        └─────────────────┘
```

## Monitoring & Logging

```
┌──────────────────────────────────────┐
│   Application Logs                   │
│  - Structured JSON logging           │
│  - Log levels: DEBUG, INFO, WARNING, │
│    ERROR, CRITICAL                   │
└──────────────┬───────────────────────┘
               │
        ┌──────▼──────────┐
        │ Log Aggregation │
        │ (Loki/ELK)      │
        └─────────────────┘
        
┌──────────────────────────────────────┐
│   Metrics                            │
│  - Response times                    │
│  - Call durations                    │
│  - Message counts                    │
│  - Active connections                │
└──────────────┬───────────────────────┘
               │
        ┌──────▼──────────┐
        │ Monitoring      │
        │ (Prometheus)    │
        └─────────────────┘
        
        ┌────────────────┐
        │ Alerting       │
        │ (Grafana)      │
        └────────────────┘
```

---

**This architecture is designed for unlimited scalability and performance.**
