"""AI Service for handling LLM interactions"""
import openai
import logging
from typing import Optional, List
from app.config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI interactions using OpenAI/Claude"""
    
    def __init__(self):
        """Initialize AI service with API keys"""
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
    
    async def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[dict]] = None,
        emotion_context: Optional[dict] = None
    ) -> dict:
        """
        Generate AI response using LLM
        
        Args:
            user_message: User's message
            conversation_history: Previous messages for context
            emotion_context: User's detected emotion
            
        Returns:
            Dictionary with response, emotion, and metadata
        """
        try:
            # Build messages list
            messages = []
            
            # Add system prompt with emotion awareness
            system_prompt = "You are Lucy, an advanced AI assistant for video calls. You are empathetic, intelligent, and engaging."
            if emotion_context:
                emotion = emotion_context.get("emotion", "neutral")
                system_prompt += f" The user currently seems {emotion}."
            
            messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history[-10:])  # Last 10 messages for context
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = await self._call_openai(messages)
            
            return {
                "response": response,
                "status": "success",
                "model": self.model
            }
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            return {
                "response": "I apologize, I'm having trouble understanding. Could you repeat that?",
                "status": "error",
                "error": str(e)
            }
    
    async def _call_openai(self, messages: List[dict]) -> str:
        """Call OpenAI API"""
        # This is synchronous, so we'll run it in a thread pool
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        def sync_call():
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=0.95,
            )
            return response.choices[0].message.content
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, sync_call)
        
        return result
    
    async def generate_avatar_behavior(self, response_text: str, emotion: str) -> dict:
        """
        Generate avatar behavior instructions based on response
        
        Args:
            response_text: The text the avatar will say
            emotion: Current emotion context
            
        Returns:
            Dictionary with avatar animation instructions
        """
        try:
            # Determine speech rate based on emotion
            emotion_config = {
                "happy": {"rate": 1.1, "pitch": 1.2, "intensity": 0.8},
                "sad": {"rate": 0.9, "pitch": 0.8, "intensity": 0.5},
                "angry": {"rate": 1.2, "pitch": 1.1, "intensity": 1.0},
                "surprised": {"rate": 1.3, "pitch": 1.3, "intensity": 0.9},
                "neutral": {"rate": 1.0, "pitch": 1.0, "intensity": 0.7},
            }
            
            config = emotion_config.get(emotion, emotion_config["neutral"])
            
            # Determine gestures based on response length and emotion
            num_words = len(response_text.split())
            gestures = self._select_gestures(num_words, emotion)
            
            return {
                "text": response_text,
                "emotion": emotion,
                "speech_config": config,
                "gestures": gestures,
                "eye_contact": True,
                "head_movement": True
            }
            
        except Exception as e:
            logger.error(f"Error generating avatar behavior: {str(e)}")
            return {
                "text": response_text,
                "emotion": "neutral",
                "error": str(e)
            }
    
    def _select_gestures(self, num_words: int, emotion: str) -> List[str]:
        """Select appropriate gestures based on word count and emotion"""
        base_gestures = ["nod", "hand_gesture", "blink", "eye_movement"]
        
        if emotion == "happy":
            return base_gestures + ["smile", "open_hands"]
        elif emotion == "angry":
            return ["frown", "pointed_gesture", "head_shake"]
        elif emotion == "sad":
            return ["sigh", "slow_nod", "downward_gaze"]
        elif emotion == "surprised":
            return ["eyebrow_raise", "open_mouth", "step_back"]
        else:
            return base_gestures
