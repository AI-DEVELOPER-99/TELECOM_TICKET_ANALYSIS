const express = require('express');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000';

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// API Proxy Endpoints
app.post('/api/analyze', async (req, res) => {
    try {
        const response = await axios.post(`${BACKEND_URL}/api/analyze`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            success: false,
            error: error.response?.data?.error || error.message
        });
    }
});

app.post('/api/search', async (req, res) => {
    try {
        const response = await axios.post(`${BACKEND_URL}/api/search`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            success: false,
            error: error.response?.data?.error || error.message
        });
    }
});

app.get('/api/stats', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/api/stats`);
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).json({
            success: false,
            error: error.response?.data?.error || error.message
        });
    }
});

app.get('/api/health', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/health`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({
            success: false,
            error: 'Backend not available'
        });
    }
});

// Serve HTML
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(PORT, () => {
    console.log(`\n${'═'.repeat(60)}`);
    console.log(`  TELECOM TICKET ANALYSIS ASSISTANT - WEB UI`);
    console.log(`${'═'.repeat(60)}\n`);
    console.log(`  🌐 Server running at: http://localhost:${PORT}`);
    console.log(`  🔗 Backend URL: ${BACKEND_URL}`);
    console.log(`\n  Press Ctrl+C to stop the server\n`);
});
