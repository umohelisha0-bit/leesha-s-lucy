import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Box, Button, Typography, Grid, Paper } from '@mui/material';
import { VideoCall as VideoCallIcon, History as HistoryIcon, Favorite as FavoriteIcon } from '@mui/icons-material';
import ApiService from '../services/apiService';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = React.useState(false);

  const startNewCall = async () => {
    try {
      setLoading(true);
      // Generate a user ID (in real app, this would come from auth)
      const userId = `user_${Date.now()}`;
      
      const response = await ApiService.startCall(userId);
      navigate(`/call/${response.call_id}`);
    } catch (error) {
      console.error('Error starting call:', error);
      alert('Failed to start call');
    } finally {
      setLoading(false);
    }
  };

  const viewHistory = () => {
    navigate('/history');
  };

  return (
    <Container maxWidth="lg" className="landing-page">
      <Box className="landing-header">
        <Typography variant="h2" component="h1" className="title">
          ✨ Leesha's Lucy
        </Typography>
        <Typography variant="h5" className="subtitle">
          Advanced AI Video Call Assistant - No Time Limits, No Watermarks
        </Typography>
      </Box>

      <Grid container spacing={4} className="features-grid">
        <Grid item xs={12} sm={6} md={3}>
          <Paper className="feature-card">
            <VideoCallIcon className="feature-icon" />
            <Typography variant="h6">Real-time Video</Typography>
            <Typography variant="body2" color="textSecondary">
              HD video calling with WebRTC
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Paper className="feature-card">
            <FavoriteIcon className="feature-icon" />
            <Typography variant="h6">Emotion Aware</Typography>
            <Typography variant="body2" color="textSecondary">
              AI detects and responds to emotions
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Paper className="feature-card">
            <VideoCallIcon className="feature-icon" />
            <Typography variant="h6">Realistic Avatar</Typography>
            <Typography variant="body2" color="textSecondary">
              Advanced 3D avatar with full expressions
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Paper className="feature-card">
            <FavoriteIcon className="feature-icon" />
            <Typography variant="h6">Unlimited</Typography>
            <Typography variant="body2" color="textSecondary">
              No time limits, no restrictions
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      <Box className="cta-section">
        <Button
          variant="contained"
          size="large"
          onClick={startNewCall}
          disabled={loading}
          className="start-button"
        >
          {loading ? 'Starting...' : '🎥 Start Video Call'}
        </Button>
        <Button
          variant="outlined"
          size="large"
          onClick={viewHistory}
          className="history-button"
        >
          <HistoryIcon /> View History
        </Button>
      </Box>

      <Box className="info-section">
        <Typography variant="body1" className="info-text">
          💡 Features: AI Conversations • Speech Recognition • Text-to-Speech • 
          Emotion Detection • Avatar Animations • Unlimited Sessions
        </Typography>
      </Box>
    </Container>
  );
};

export default LandingPage;
