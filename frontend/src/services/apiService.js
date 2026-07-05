import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const ApiService = {
  // Call endpoints
  startCall: async (userId) => {
    const response = await axios.post(`${API_URL}/api/calls/start`, null, {
      params: { user_id: userId },
    });
    return response.data;
  },

  getCall: async (callId) => {
    const response = await axios.get(`${API_URL}/api/calls/${callId}`);
    return response.data;
  },

  endCall: async (callId) => {
    const response = await axios.post(`${API_URL}/api/calls/${callId}/end`);
    return response.data;
  },

  getCallSessions: async (callId) => {
    const response = await axios.get(`${API_URL}/api/calls/${callId}/sessions`);
    return response.data;
  },

  // AI endpoints
  chat: async (message, emotionContext = null) => {
    const response = await axios.post(`${API_URL}/api/ai/chat`, null, {
      params: {
        message,
        emotion_context: emotionContext ? JSON.stringify(emotionContext) : null,
      },
    });
    return response.data;
  },

  transcribeAudio: async (audioFile) => {
    const formData = new FormData();
    formData.append('file', audioFile);
    const response = await axios.post(`${API_URL}/api/ai/voice/transcribe`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  synthesizeSpeech: async (text, emotion = 'neutral') => {
    const response = await axios.post(`${API_URL}/api/ai/voice/synthesize`, null, {
      params: { text, emotion },
    });
    return response.data;
  },

  initializeAvatar: async (preferences = null) => {
    const response = await axios.get(`${API_URL}/api/ai/avatar/init`, {
      params: { user_preferences: preferences ? JSON.stringify(preferences) : null },
    });
    return response.data;
  },

  updateAvatarState: async (emotion, action, expression = null) => {
    const response = await axios.post(`${API_URL}/api/ai/avatar/update-state`, null, {
      params: { emotion, action, expression },
    });
    return response.data;
  },

  detectEmotionFromFace: async (imageFile) => {
    const formData = new FormData();
    formData.append('file', imageFile);
    const response = await axios.post(`${API_URL}/api/ai/emotion/detect-face`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  detectEmotionFromVoice: async (audioFile) => {
    const formData = new FormData();
    formData.append('file', audioFile);
    const response = await axios.post(`${API_URL}/api/ai/emotion/detect-voice`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  detectEmotionFromText: async (text) => {
    const response = await axios.post(`${API_URL}/api/ai/emotion/detect-text`, null, {
      params: { text },
    });
    return response.data;
  },

  // Analytics endpoints
  getCallHistory: async (userId = null, limit = 50) => {
    const response = await axios.get(`${API_URL}/api/analytics/calls`, {
      params: { user_id: userId, limit },
    });
    return response.data;
  },

  getStatistics: async (userId = null, days = 30) => {
    const response = await axios.get(`${API_URL}/api/analytics/stats`, {
      params: { user_id: userId, days },
    });
    return response.data;
  },

  getCallMessages: async (callId, limit = 100) => {
    const response = await axios.get(`${API_URL}/api/analytics/messages/${callId}`, {
      params: { limit },
    });
    return response.data;
  },
};

export default ApiService;
