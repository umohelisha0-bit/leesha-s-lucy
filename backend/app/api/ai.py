"""AI service endpoints"""
import logging
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from app.services import AIService, SpeechService, AvatarService, EmotionService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
ai_service = AIService()
speech_service = SpeechService()
avatar_service = AvatarService()
emotion_service = EmotionService()


@router.post("/chat")
async def chat(message: str, emotion_context: dict = None):
    """
    Send message to AI and get response
    """
    try:
        response = await ai_service.generate_response(
            user_message=message,
            emotion_context=emotion_context
        )
        
        return {
            "message": message,
            "response": response["response"],
            "status": response["status"]
        }
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio to text
    """
    try:
        audio_data = await file.read()
        result = await speech_service.transcribe_audio(audio_data)
        
        return {
            "text": result["text"],
            "confidence": result["confidence"],
            "status": result["status"]
        }
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice/synthesize")
async def synthesize_speech(text: str, emotion: str = "neutral"):
    """
    Convert text to speech
    """
    try:
        audio_bytes, metadata = await speech_service.synthesize_speech(
            text=text,
            emotion=emotion
        )
        
        if not audio_bytes:
            raise HTTPException(status_code=500, detail="Failed to synthesize speech")
        
        return {
            "audio_size": len(audio_bytes),
            "text": text,
            "emotion": emotion,
            "status": metadata["status"]
        }
    except Exception as e:
        logger.error(f"Error synthesizing speech: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/avatar/init")
async def initialize_avatar(user_preferences: dict = None):
    """
    Initialize avatar for call
    """
    try:
        avatar_config = await avatar_service.initialize_avatar(user_preferences)
        
        return avatar_config
    except Exception as e:
        logger.error(f"Error initializing avatar: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/avatar/update-state")
async def update_avatar_state(emotion: str, action: str, expression: str = None):
    """
    Update avatar state (emotion, expression, animation)
    """
    try:
        state = await avatar_service.update_avatar_state(
            emotion=emotion,
            action=action,
            expression=expression
        )
        
        return state
    except Exception as e:
        logger.error(f"Error updating avatar state: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/avatar/gesture")
async def animate_gesture(gesture_type: str, intensity: float = 0.7):
    """
    Animate a specific gesture
    """
    try:
        animation = await avatar_service.animate_gesture(
            gesture_type=gesture_type,
            intensity=intensity
        )
        
        return animation
    except Exception as e:
        logger.error(f"Error animating gesture: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/emotion/detect-face")
async def detect_emotion_from_face(file: UploadFile = File(...)):
    """
    Detect emotion from facial image
    """
    try:
        image_data = await file.read()
        result = await emotion_service.detect_emotion_from_face(image_data)
        
        return result
    except Exception as e:
        logger.error(f"Error detecting emotion from face: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/emotion/detect-voice")
async def detect_emotion_from_voice(file: UploadFile = File(...)):
    """
    Detect emotion from voice
    """
    try:
        audio_data = await file.read()
        result = await emotion_service.detect_emotion_from_voice(audio_data)
        
        return result
    except Exception as e:
        logger.error(f"Error detecting emotion from voice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/emotion/detect-text")
async def detect_emotion_from_text(text: str):
    """
    Analyze emotion from text (sentiment analysis)
    """
    try:
        result = await emotion_service.analyze_text_emotion(text)
        
        return result
    except Exception as e:
        logger.error(f"Error detecting emotion from text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
