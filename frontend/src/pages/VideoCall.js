import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Box, Button, Paper, TextField, Typography, Avatar, CircularProgress } from '@mui/material';
import { Send as SendIcon, Mic as MicIcon, Phone as PhoneIcon, ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import AvatarDisplay from '../components/AvatarDisplay';
import ApiService from '../services/apiService';
import WebSocketService from '../services/websocketService';
import './VideoCall.css';

const VideoCall = () => {
  const { callId } = useParams();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [callDuration, setCallDuration] = useState(0);
  const [avatarEmotion, setAvatarEmotion] = useState('neutral');
  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const wsRef = useRef(null);
  const callStartTimeRef = useRef(Date.now());

  // Initialize WebSocket and call
  useEffect(() => {
    const initializeCall = async () => {
      try {
        // Connect WebSocket
        const connectionId = `conn_${Date.now()}`;
        wsRef.current = new WebSocketService(
          callId,
          connectionId,
          handleWebSocketMessage
        );
        await wsRef.current.connect();
      } catch (error) {
        console.error('Error initializing call:', error);
      }
    };

    initializeCall();

    return () => {
      if (wsRef.current) {
        wsRef.current.disconnect();
      }
    };
  }, [callId]);

  // Update call duration
  useEffect(() => {
    const interval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - callStartTimeRef.current) / 1000);
      setCallDuration(elapsed);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleWebSocketMessage = (message) => {
    if (message.type === 'chat_response') {
      setMessages((prev) => [
        ...prev,
        {
          id: message.message_id,
          sender: 'AI',
          content: message.content,
          timestamp: new Date(message.timestamp),
        },
      ]);
      
      // Update avatar emotion if available
      if (message.avatar_behavior?.emotion) {
        setAvatarEmotion(message.avatar_behavior.emotion);
      }
    } else if (message.type === 'emotion_detected') {
      setAvatarEmotion(message.emotion);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: `msg_${Date.now()}`,
      sender: 'You',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      if (wsRef.current && wsRef.current.isConnected) {
        wsRef.current.send({
          type: 'chat',
          content: inputValue,
          emotion_context: { emotion: avatarEmotion },
          history: messages.map((m) => ({
            role: m.sender === 'You' ? 'user' : 'assistant',
            content: m.content,
          })),
        });
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      const chunks = [];

      mediaRecorderRef.current.ondataavailable = (e) => {
        chunks.push(e.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        sendVoiceMessage(blob);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const sendVoiceMessage = async (audioBlob) => {
    try {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64Audio = reader.result.split(',')[1];
        if (wsRef.current && wsRef.current.isConnected) {
          wsRef.current.send({
            type: 'voice',
            audio_data: base64Audio,
          });
        }
      };
      reader.readAsDataURL(audioBlob);
    } catch (error) {
      console.error('Error sending voice message:', error);
    }
  };

  const endCall = async () => {
    try {
      await ApiService.endCall(callId);
      navigate('/');
    } catch (error) {
      console.error('Error ending call:', error);
    }
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${
      minutes.toString().padStart(2, '0')
    }:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Container maxWidth="lg" className="video-call">
      <Box className="call-header">
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/')}>
          Back
        </Button>
        <Typography variant="h6">Call Duration: {formatTime(callDuration)}</Typography>
        <Button
          variant="contained"
          color="error"
          startIcon={<PhoneIcon />}
          onClick={endCall}
        >
          End Call
        </Button>
      </Box>

      <Box className="call-content">
        <Box className="avatar-section">
          <Paper className="avatar-container">
            <AvatarDisplay emotion={avatarEmotion} />
          </Paper>
          <Typography variant="body2" className="avatar-label">
            Lucy - AI Assistant
          </Typography>
        </Box>

        <Paper className="chat-section">
          <Box className="messages-container">
            {messages.map((msg) => (
              <Box
                key={msg.id}
                className={`message ${msg.sender === 'You' ? 'user' : 'ai'}`}
              >
                <Box className="message-bubble">
                  <Typography variant="body2">{msg.content}</Typography>
                  <Typography variant="caption" className="timestamp">
                    {msg.timestamp.toLocaleTimeString()}
                  </Typography>
                </Box>
              </Box>
            ))}
            <div ref={messagesEndRef} />
          </Box>

          <Box className="input-section">
            <TextField
              fullWidth
              placeholder="Type your message..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              disabled={isLoading || isRecording}
            />
            <Button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim() || isRecording}
              variant="contained"
              endIcon={isLoading ? <CircularProgress size={20} /> : <SendIcon />}
            >
              Send
            </Button>
            <Button
              onClick={isRecording ? stopRecording : startRecording}
              variant={isRecording ? 'contained' : 'outlined'}
              color={isRecording ? 'error' : 'primary'}
              startIcon={<MicIcon />}
            >
              {isRecording ? 'Stop' : 'Voice'}
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default VideoCall;
