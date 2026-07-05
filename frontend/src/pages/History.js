import React, { useState, useEffect } from 'react';
import { Container, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, Button, Typography } from '@mui/material';
import { ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import ApiService from '../services/apiService';
import './History.css';

const History = () => {
  const navigate = useNavigate();
  const [calls, setCalls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const callsData = await ApiService.getCallHistory();
      const statsData = await ApiService.getStatistics();
      setCalls(callsData.calls);
      setStats(statsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const formatDuration = (seconds) => {
    if (!seconds) return '—';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}h ${minutes}m ${secs}s`;
  };

  return (
    <Container maxWidth="lg" className="history-page">
      <Box className="history-header">
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/')}
          variant="outlined"
        >
          Back to Home
        </Button>
        <Typography variant="h4">Call History & Statistics</Typography>
      </Box>

      {stats && (
        <Box className="stats-section">
          <Paper className="stat-card">
            <Typography variant="h6">Total Calls</Typography>
            <Typography variant="h3" className="stat-value">
              {stats.total_calls}
            </Typography>
          </Paper>
          <Paper className="stat-card">
            <Typography variant="h6">Active Calls</Typography>
            <Typography variant="h3" className="stat-value">
              {stats.active_calls}
            </Typography>
          </Paper>
          <Paper className="stat-card">
            <Typography variant="h6">Total Duration</Typography>
            <Typography variant="h3" className="stat-value">
              {Math.floor(stats.total_duration_seconds / 3600)}h
            </Typography>
          </Paper>
          <Paper className="stat-card">
            <Typography variant="h6">Total Messages</Typography>
            <Typography variant="h3" className="stat-value">
              {stats.total_messages}
            </Typography>
          </Paper>
        </Box>
      )}

      <Box className="features-highlight">
        <Typography variant="h6">✨ Unlimited Features:</Typography>
        <Typography variant="body2">
          No Time Limits • No Session Timeout • No Watermarks • Unlimited Messages
        </Typography>
      </Box>

      <TableContainer component={Paper} className="calls-table">
        <Table>
          <TableHead>
            <TableRow className="table-header">
              <TableCell>Call ID</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Started</TableCell>
              <TableCell>Ended</TableCell>
              <TableCell>Duration</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {calls.length > 0 ? (
              calls.map((call) => (
                <TableRow key={call.call_id} className="table-row">
                  <TableCell className="call-id">{call.call_id.substring(0, 8)}...</TableCell>
                  <TableCell>
                    <span className={`status ${call.status}`}>{call.status}</span>
                  </TableCell>
                  <TableCell>{formatDate(call.started_at)}</TableCell>
                  <TableCell>{call.ended_at ? formatDate(call.ended_at) : 'Ongoing'}</TableCell>
                  <TableCell>{formatDuration(call.duration_seconds)}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={5} align="center" className="no-data">
                  No calls yet. Start one now!
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default History;
