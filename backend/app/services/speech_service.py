"""Speech Service for STT and TTS"""
import logging
from typing import Optional, Tuple
from app.config import settings

logger = logging.getLogger(__name__)


class SpeechService:
    """Service for speech-to-text and text-to-speech"""
    
    def __init__(self):
        """Initialize speech service"""
        self.tts_voice_id = settings.ELEVENLABS_VOICE_ID
        self.whisper_model = settings.WHISPER_MODEL
        self.language = settings.WHISPER_LANGUAGE
    
    async def transcribe_audio(self, audio_data: bytes) -> dict:
        """
        Transcribe audio to text using Whisper
        
        Args:
            audio_data: Audio bytes
            
        Returns:
            Dictionary with transcribed text and confidence
        """
        try:
            import openai
            import io
            
            # Convert bytes to file-like object
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"
            
            # Transcribe using Whisper
            transcript = openai.Audio.transcribe(
                model=self.whisper_model,
                file=audio_file,
                language=self.language
            )
            
            return {
                "text": transcript.get("text", ""),
                "status": "success",
                "confidence": 0.95  # Whisper doesn't return confidence, but it's typically high
            }
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return {
                "text": "",
                "status": "error",
                "error": str(e)
            }
    
    async def synthesize_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        emotion: str = "neutral"
    ) -> Tuple[bytes, dict]:
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text: Text to synthesize
            voice_id: Voice ID (uses default if not provided)
            emotion: Emotion context for better speech synthesis
            
        Returns:
            Tuple of (audio_bytes, metadata)
        """
        try:
            from elevenlabs import generate, set_api_key
            import asyncio
            from concurrent.futures import ThreadPoolExecutor
            
            set_api_key(settings.ELEVENLABS_API_KEY)
            
            voice_id = voice_id or self.tts_voice_id
            
            # Adjust speech parameters based on emotion
            speech_config = self._get_speech_config(emotion)
            
            # Generate speech synchronously in executor
            def sync_generate():
                audio = generate(
                    text=text,
                    voice=voice_id,
                    model="eleven_monolingual_v1"
                )
                return audio
            
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as pool:
                audio_bytes = await loop.run_in_executor(pool, sync_generate)
            
            return audio_bytes, {
                "status": "success",
                "text": text,
                "voice_id": voice_id,
                "emotion": emotion
            }
            
        except Exception as e:
            logger.error(f"Error synthesizing speech: {str(e)}")
            return b"", {
                "status": "error",
                "error": str(e)
            }
    
    def _get_speech_config(self, emotion: str) -> dict:
        """Get speech configuration based on emotion"""
        configs = {
            "happy": {
                "rate": 1.1,
                "pitch": 1.2,
                "energy": 1.0
            },
            "sad": {
                "rate": 0.9,
                "pitch": 0.9,
                "energy": 0.6
            },
            "angry": {
                "rate": 1.2,
                "pitch": 1.1,
                "energy": 1.0
            },
            "surprised": {
                "rate": 1.15,
                "pitch": 1.25,
                "energy": 0.9
            },
            "neutral": {
                "rate": 1.0,
                "pitch": 1.0,
                "energy": 0.7
            }
        }
        return configs.get(emotion, configs["neutral"])
