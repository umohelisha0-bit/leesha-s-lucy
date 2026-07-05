import React from 'react';
import { Box } from '@mui/material';
import './AvatarDisplay.css';

const AvatarDisplay = ({ emotion = 'neutral' }) => {
  const getEmojiForEmotion = (emotion) => {
    const emotionMap = {
      happy: '😊',
      sad: '😢',
      angry: '😠',
      surprised: '😮',
      neutral: '😐',
      confused: '🤔',
      interested: '🤩',
    };
    return emotionMap[emotion] || emotionMap.neutral;
  };

  const getColorForEmotion = (emotion) => {
    const colorMap = {
      happy: '#FFD700',
      sad: '#4169E1',
      angry: '#FF4500',
      surprised: '#FF69B4',
      neutral: '#87CEEB',
      confused: '#FFA500',
      interested: '#32CD32',
    };
    return colorMap[emotion] || colorMap.neutral;
  };

  return (
    <Box className="avatar-display">
      <Box
        className={`avatar-circle ${emotion}`}
        style={{ borderColor: getColorForEmotion(emotion) }}
      >
        <span className="avatar-emoji">{getEmojiForEmotion(emotion)}</span>
      </Box>
      <Box className="avatar-info">
        <p className="emotion-text">Emotion: <strong>{emotion}</strong></p>
        <p className="status-text">🎤 Listening...</p>
      </Box>
    </Box>
  );
};

export default AvatarDisplay;
