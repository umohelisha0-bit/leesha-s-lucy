# Leesha's Lucy - Advanced AI Video Call Software

A cutting-edge full-body video calling AI software with realistic avatars, natural conversations, and emotional intelligence.

## Features

- 🎥 Real-time HD video calling with WebRTC
- 🤖 Advanced AI conversation engine with LLM
- 🎤 Real-time speech recognition (STT)
- 🔊 Natural text-to-speech synthesis
- 😊 Emotion detection and adaptive responses
- 👤 Realistic AI avatar with full-body tracking
- ⚡ Low-latency real-time communication
- 📊 Call analytics and history
- 🌐 Scalable cloud deployment
- ∞ **Unlimited session duration - NO TIME LIMITS**
- 🎨 **No watermarks - fully customizable**

## Project Structure

```
leesha-s-lucy/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   ├── ws/          # WebSocket handlers
│   │   ├── config.py    # Configuration
│   │   ├── database.py  # Database setup
│   │   └── main.py      # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/            # React web application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   ├── hooks/       # Custom React hooks
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── docs/               # Documentation
```

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- GPU (recommended for AI models)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/umohelisha0-bit/leesha-s-lucy.git
cd leesha-s-lucy
```

2. **Setup Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Setup Frontend**
```bash
cd frontend
npm install
```

4. **Configure Environment**
```bash
cp backend/.env.example backend/.env
# Edit .env with your API keys
```

5. **Run with Docker Compose**
```bash
docker-compose up --build
```

## API Documentation

Once running, visit:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## Configuration

### Environment Variables

See `backend/.env.example` for all available options:
- OpenAI/Claude API keys
- ElevenLabs TTS key
- Database credentials
- etc.

## Technology Stack

**Backend:**
- FastAPI (async web framework)
- Uvicorn (ASGI server)
- SQLAlchemy (ORM)
- WebSockets (real-time)
- PyAudio, librosa (audio processing)
- OpenCV (video processing)
- PyTorch/TensorFlow (ML models)

**Frontend:**
- React 18
- React Router
- Socket.io (WebSocket client)
- TensorFlow.js (client-side ML)
- Three.js (3D avatar rendering)
- Material-UI (components)

**AI/ML:**
- OpenAI Whisper (speech recognition)
- GPT-4/Claude (language model)
- ElevenLabs (text-to-speech)
- MediaPipe (pose/emotion detection)
- Custom GAN (avatar generation)

**DevOps:**
- Docker & Docker Compose
- PostgreSQL (database)
- Redis (caching/queue)
- Nginx (reverse proxy)

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm start
```

## API Endpoints

### Video Calls
- `POST /api/calls/start` - Start a new call
- `GET /api/calls/{call_id}` - Get call details
- `POST /api/calls/{call_id}/end` - End call
- `WS /ws/call/{call_id}` - WebSocket for real-time data

### AI Services
- `POST /api/ai/chat` - Send message to AI
- `POST /api/ai/voice` - Voice input processing
- `GET /api/ai/avatar` - Get avatar data
- `POST /api/ai/emotion` - Emotion detection

### Analytics
- `GET /api/analytics/calls` - Call history
- `GET /api/analytics/stats` - Usage statistics

## Deployment

### Docker Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Deployment
- AWS EC2 with load balancing
- Google Cloud Run for serverless
- Azure Container Instances
- See `docs/deployment.md` for detailed guides

## Performance Optimization

- Async/await for non-blocking I/O
- Connection pooling
- Caching with Redis
- CDN for static assets
- GPU acceleration for AI models
- Batch processing for inference
- Unlimited session duration for long conversations

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

MIT License - see LICENSE file

## Support

For issues and questions, open a GitHub issue or contact us.

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Multi-party group calls
- [ ] Advanced avatar customization
- [ ] Gesture recognition
- [ ] Real-time translation
- [ ] Screen sharing
- [ ] Recording & playback
- [ ] Analytics dashboard
- [ ] Custom avatar training
- [ ] Voice cloning

---

Built with ❤️ by Leesha
