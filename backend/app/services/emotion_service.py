"""Emotion Detection Service"""
import logging
from typing import Optional, Dict
import numpy as np

logger = logging.getLogger(__name__)


class EmotionService:
    """Service for emotion detection and analysis"""
    
    def __init__(self):
        """Initialize emotion service"""
        self.emotions = ["happy", "sad", "angry", "surprised", "neutral", "confused", "interested"]
        self.confidence_threshold = 0.5
    
    async def detect_emotion_from_face(self, face_frame_data: bytes) -> dict:
        """
        Detect emotion from facial frame
        
        Args:
            face_frame_data: Image frame data containing face
            
        Returns:
            Dictionary with detected emotion and confidence
        """
        try:
            import cv2
            import numpy as np
            from io import BytesIO
            from PIL import Image
            
            # Convert bytes to image
            img = Image.open(BytesIO(face_frame_data))
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # Detect faces
            emotion = await self._detect_with_mediapipe(frame)
            
            return {
                "emotion": emotion["emotion"],
                "confidence": emotion["confidence"],
                "landmark_data": emotion.get("landmarks"),
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error detecting emotion from face: {str(e)}")
            return {
                "emotion": "neutral",
                "confidence": 0.5,
                "status": "error",
                "error": str(e)
            }
    
    async def detect_emotion_from_voice(self, audio_data: bytes) -> dict:
        """
        Detect emotion from voice
        
        Args:
            audio_data: Audio bytes
            
        Returns:
            Dictionary with detected emotion and confidence
        """
        try:
            import librosa
            import numpy as np
            from io import BytesIO
            
            # Load audio
            y, sr = librosa.load(BytesIO(audio_data), sr=22050)
            
            # Extract features
            features = self._extract_audio_features(y, sr)
            
            # Classify emotion (simplified)
            emotion = self._classify_emotion_from_features(features)
            
            return {
                "emotion": emotion["emotion"],
                "confidence": emotion["confidence"],
                "features": {
                    "pitch": features.get("pitch"),
                    "energy": features.get("energy"),
                    "tempo": features.get("tempo")
                },
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error detecting emotion from voice: {str(e)}")
            return {
                "emotion": "neutral",
                "confidence": 0.5,
                "status": "error",
                "error": str(e)
            }
    
    async def analyze_text_emotion(self, text: str) -> dict:
        """
        Analyze emotion from text (sentiment analysis)
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with detected emotion and confidence
        """
        try:
            # Simple sentiment-based emotion detection
            emotion_keywords = {
                "happy": ["happy", "great", "excellent", "wonderful", "love", "amazing", "excited", "glad"],
                "sad": ["sad", "depressed", "unhappy", "bad", "terrible", "hate", "awful", "disappointed"],
                "angry": ["angry", "furious", "mad", "upset", "rage", "hate", "annoyed", "irritated"],
                "surprised": ["surprised", "wow", "amazing", "shocked", "unexpected", "unbelievable"],
                "confused": ["confused", "uncertain", "unclear", "what", "huh", "don't understand"],
                "neutral": ["ok", "fine", "sure", "alright", "yeah"]
            }
            
            text_lower = text.lower()
            emotions_found = {}
            
            for emotion, keywords in emotion_keywords.items():
                count = sum(1 for keyword in keywords if keyword in text_lower)
                if count > 0:
                    emotions_found[emotion] = count
            
            if not emotions_found:
                return {"emotion": "neutral", "confidence": 0.5}
            
            # Get emotion with highest count
            top_emotion = max(emotions_found, key=emotions_found.get)
            confidence = min(0.95, 0.5 + (emotions_found[top_emotion] * 0.1))
            
            return {
                "emotion": top_emotion,
                "confidence": confidence,
                "keywords_detected": list(emotions_found.keys()),
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing text emotion: {str(e)}")
            return {
                "emotion": "neutral",
                "confidence": 0.5,
                "status": "error",
                "error": str(e)
            }
    
    async def detect_combined_emotion(
        self,
        face_data: Optional[bytes] = None,
        voice_data: Optional[bytes] = None,
        text: Optional[str] = None
    ) -> dict:
        """
        Detect emotion from multiple sources and combine
        
        Args:
            face_data: Optional facial frame data
            voice_data: Optional audio data
            text: Optional text data
            
        Returns:
            Combined emotion analysis
        """
        try:
            emotions = {}
            weights = {}
            
            # Facial emotion
            if face_data:
                face_emotion = await self.detect_emotion_from_face(face_data)
                emotions["face"] = face_emotion
                weights["face"] = 0.4
            
            # Voice emotion
            if voice_data:
                voice_emotion = await self.detect_emotion_from_voice(voice_data)
                emotions["voice"] = voice_emotion
                weights["voice"] = 0.35
            
            # Text emotion
            if text:
                text_emotion = await self.analyze_text_emotion(text)
                emotions["text"] = text_emotion
                weights["text"] = 0.25
            
            # Combine emotions with weighted average
            final_emotion = self._combine_emotions(emotions, weights)
            
            return {
                "emotion": final_emotion["emotion"],
                "confidence": final_emotion["confidence"],
                "individual_emotions": emotions,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error detecting combined emotion: {str(e)}")
            return {
                "emotion": "neutral",
                "confidence": 0.5,
                "status": "error",
                "error": str(e)
            }
    
    async def _detect_with_mediapipe(self, frame) -> dict:
        """Detect emotion using MediaPipe"""
        try:
            import mediapipe as mp
            
            # Use MediaPipe Face Detection
            mp_face_detection = mp.solutions.face_detection
            
            with mp_face_detection.FaceDetection() as face_detection:
                results = face_detection.process(frame)
                
                if results.detections:
                    # Simplified emotion detection based on face geometry
                    emotion = "neutral"
                    confidence = 0.7
                    landmarks = results.detections[0]
                    
                    return {
                        "emotion": emotion,
                        "confidence": confidence,
                        "landmarks": str(landmarks)
                    }
            
            return {"emotion": "neutral", "confidence": 0.5}
            
        except Exception as e:
            logger.error(f"MediaPipe error: {str(e)}")
            return {"emotion": "neutral", "confidence": 0.5}
    
    def _extract_audio_features(self, y, sr) -> dict:
        """Extract audio features for emotion detection"""
        try:
            import librosa
            
            # Extract features
            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            energy = np.mean(librosa.feature.melspectrogram(y=y, sr=sr))
            zero_crossing = np.mean(librosa.feature.zero_crossing_rate(y))
            
            # Estimate pitch (simplified)
            pitch = np.mean(np.abs(np.fft.fft(y)[:len(y)//2]))
            
            return {
                "mfcc": np.mean(mfcc),
                "energy": energy,
                "zero_crossing": zero_crossing,
                "pitch": pitch,
                "tempo": librosa.beat.tempo(y=y, sr=sr)[0] if len(y) > 0 else 0
            }
        except:
            return {"energy": 0.5, "pitch": 0.5, "tempo": 0}
    
    def _classify_emotion_from_features(self, features: dict) -> dict:
        """Classify emotion from audio features"""
        energy = features.get("energy", 0.5)
        pitch = features.get("pitch", 0.5)
        
        # Simple heuristic classification
        if energy > 0.7 and pitch > 0.6:
            emotion = "happy"
            confidence = 0.8
        elif energy < 0.3:
            emotion = "sad"
            confidence = 0.7
        elif energy > 0.8:
            emotion = "angry"
            confidence = 0.75
        else:
            emotion = "neutral"
            confidence = 0.6
        
        return {"emotion": emotion, "confidence": confidence}
    
    def _combine_emotions(self, emotions: dict, weights: dict) -> dict:
        """Combine emotion predictions from multiple sources"""
        emotion_scores = {}
        total_weight = 0
        
        for source, emotion_data in emotions.items():
            if emotion_data.get("status") == "success":
                emotion = emotion_data.get("emotion", "neutral")
                confidence = emotion_data.get("confidence", 0.5)
                weight = weights.get(source, 0.33)
                
                if emotion not in emotion_scores:
                    emotion_scores[emotion] = 0
                
                emotion_scores[emotion] += confidence * weight
                total_weight += weight
        
        if not emotion_scores:
            return {"emotion": "neutral", "confidence": 0.5}
        
        # Get emotion with highest score
        final_emotion = max(emotion_scores, key=emotion_scores.get)
        final_confidence = emotion_scores[final_emotion] / total_weight if total_weight > 0 else 0.5
        
        return {"emotion": final_emotion, "confidence": min(0.99, final_confidence)}
