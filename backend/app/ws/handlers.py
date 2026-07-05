"""WebSocket handlers for real-time communication"""
import logging
import json
from fastapi import WebSocket, WebSocketDisconnect
from app.ws.manager import connection_manager
from app.services import AIService, SpeechService, AvatarService, EmotionService
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

# Initialize services
ai_service = AIService()
speech_service = SpeechService()
avatar_service = AvatarService()
emotion_service = EmotionService()


async def call_handler(websocket: WebSocket, call_id: str, connection_id: str):
    """
    Handle WebSocket connection for video calls
    """
    await websocket.accept()
    
    try:
        # Add connection to manager
        await connection_manager.connect(call_id, connection_id, websocket)
        
        # Send welcome message
        await websocket.send_json({
            "type": "connection_established",
            "connection_id": connection_id,
            "call_id": call_id,
            "timestamp": datetime.utcnow().isoformat(),
            "features": {
                "unlimited_duration": True,
                "no_watermark": True,
                "emotion_detection": True
            }
        })
        
        # Listen for messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            await handle_message(call_id, connection_id, message, websocket)
    
    except WebSocketDisconnect:
        logger.info(f"Client {connection_id} disconnected from call {call_id}")
        await connection_manager.disconnect(call_id, connection_id)
    
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await connection_manager.disconnect(call_id, connection_id)


async def handle_message(call_id: str, connection_id: str, message: dict, websocket: WebSocket):
    """
    Handle different types of WebSocket messages
    """
    try:
        msg_type = message.get("type")
        
        if msg_type == "chat":
            await handle_chat_message(call_id, connection_id, message, websocket)
        
        elif msg_type == "voice":
            await handle_voice_message(call_id, connection_id, message, websocket)
        
        elif msg_type == "emotion":
            await handle_emotion_message(call_id, connection_id, message, websocket)
        
        elif msg_type == "avatar_request":
            await handle_avatar_request(call_id, connection_id, message, websocket)
        
        elif msg_type == "heartbeat":
            await websocket.send_json({
                "type": "heartbeat_ack",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        else:
            logger.warning(f"Unknown message type: {msg_type}")
    
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "error": str(e)
        })


async def handle_chat_message(call_id: str, connection_id: str, message: dict, websocket: WebSocket):
    """
    Handle chat messages from user
    """
    try:
        user_message = message.get("content")
        emotion_context = message.get("emotion_context")
        conversation_history = message.get("history", [])
        
        # Get AI response
        ai_response = await ai_service.generate_response(
            user_message=user_message,
            conversation_history=conversation_history,
            emotion_context=emotion_context
        )
        
        # Get avatar behavior
        behavior = await ai_service.generate_avatar_behavior(
            response_text=ai_response["response"],
            emotion=emotion_context.get("emotion", "neutral") if emotion_context else "neutral"
        )
        
        # Send response back
        response_message = {
            "type": "chat_response",
            "message_id": str(uuid.uuid4()),
            "content": ai_response["response"],
            "avatar_behavior": behavior,
            "timestamp": datetime.utcnow().isoformat(),
            "connection_id": connection_id
        }
        
        # Broadcast to all connections in call
        await connection_manager.broadcast(call_id, response_message)
        
        logger.info(f"Chat message processed for call {call_id}")
    
    except Exception as e:
        logger.error(f"Error handling chat message: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "error": f"Failed to process chat: {str(e)}"
        })


async def handle_voice_message(call_id: str, connection_id: str, message: dict, websocket: WebSocket):
    """
    Handle voice messages (audio data)
    """
    try:
        audio_data = message.get("audio_data")  # Base64 encoded
        import base64
        
        audio_bytes = base64.b64decode(audio_data)
        
        # Transcribe audio
        transcription = await speech_service.transcribe_audio(audio_bytes)
        
        if transcription["status"] == "success":
            # Process as chat message
            ai_response = await ai_service.generate_response(
                user_message=transcription["text"]
            )
            
            # Synthesize speech response
            audio_response, tts_metadata = await speech_service.synthesize_speech(
                text=ai_response["response"]
            )
            
            # Encode audio response
            audio_b64 = base64.b64encode(audio_response).decode()
            
            response_message = {
                "type": "voice_response",
                "message_id": str(uuid.uuid4()),
                "transcription": transcription["text"],
                "response_text": ai_response["response"],
                "response_audio": audio_b64,
                "timestamp": datetime.utcnow().isoformat(),
                "connection_id": connection_id
            }
            
            await connection_manager.broadcast(call_id, response_message)
            logger.info(f"Voice message processed for call {call_id}")
    
    except Exception as e:
        logger.error(f"Error handling voice message: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "error": f"Failed to process voice: {str(e)}"
        })


async def handle_emotion_message(call_id: str, connection_id: str, message: dict, websocket: WebSocket):
    """
    Handle emotion detection requests
    """
    try:
        emotion_type = message.get("emotion_type")  # face, voice, or text
        data = message.get("data")
        
        if emotion_type == "face":
            import base64
            image_bytes = base64.b64decode(data)
            emotion_result = await emotion_service.detect_emotion_from_face(image_bytes)
        
        elif emotion_type == "voice":
            import base64
            audio_bytes = base64.b64decode(data)
            emotion_result = await emotion_service.detect_emotion_from_voice(audio_bytes)
        
        elif emotion_type == "text":
            emotion_result = await emotion_service.analyze_text_emotion(data)
        
        else:
            emotion_result = {"status": "error", "error": "Invalid emotion type"}
        
        # Send emotion detection result
        response_message = {
            "type": "emotion_detected",
            "emotion": emotion_result.get("emotion"),
            "confidence": emotion_result.get("confidence"),
            "timestamp": datetime.utcnow().isoformat(),
            "connection_id": connection_id
        }
        
        await connection_manager.broadcast(call_id, response_message)
        logger.info(f"Emotion detected for call {call_id}: {emotion_result.get('emotion')}")
    
    except Exception as e:
        logger.error(f"Error handling emotion message: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "error": f"Failed to detect emotion: {str(e)}"
        })


async def handle_avatar_request(call_id: str, connection_id: str, message: dict, websocket: WebSocket):
    """
    Handle avatar-related requests
    """
    try:
        request_type = message.get("request_type")  # init, update, gesture
        
        if request_type == "init":
            preferences = message.get("preferences")
            avatar_config = await avatar_service.initialize_avatar(preferences)
        
        elif request_type == "update":
            emotion = message.get("emotion", "neutral")
            action = message.get("action", "idle")
            expression = message.get("expression")
            avatar_config = await avatar_service.update_avatar_state(emotion, action, expression)
        
        elif request_type == "gesture":
            gesture_type = message.get("gesture_type")
            intensity = message.get("intensity", 0.7)
            avatar_config = await avatar_service.animate_gesture(gesture_type, intensity)
        
        else:
            avatar_config = {"status": "error", "error": "Invalid request type"}
        
        # Send avatar configuration
        response_message = {
            "type": "avatar_config",
            "avatar_config": avatar_config,
            "timestamp": datetime.utcnow().isoformat(),
            "connection_id": connection_id
        }
        
        await connection_manager.broadcast(call_id, response_message)
        logger.info(f"Avatar request processed for call {call_id}")
    
    except Exception as e:
        logger.error(f"Error handling avatar request: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "error": f"Failed to process avatar request: {str(e)}"
        })
