import express from 'express';
import cors from 'cors';
import axios from 'axios';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config();

const app = express();

// Enhanced CORS configuration
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type']
}));

app.use(express.json());

const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434';

// Model-specific configurations
const MODEL_CONFIGS = {
  'mxbai-embed-large': { temperature: 0.7, top_p: 0.9 },
  'minicpm-v': { temperature: 0.8, top_p: 0.9 },
  'qwen2.5-coder': { temperature: 0.6, top_p: 0.95 },
  'codegemma': { temperature: 0.6, top_p: 0.95 },
  'codellama': { temperature: 0.7, top_p: 0.95 },
  'llama3.2-vision': { temperature: 0.8, top_p: 0.9 }
};

// Add these right after your app.use() statements
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    ollama: 'running',
    model: 'minicpm-v'
  });
});

// Add a root endpoint
app.get('/', (req, res) => {
  res.status(200).json({
    message: 'Aide AI Backend Service',
    version: '1.0'
  });
});

// Update the chat endpoint
app.post('/api/chat', async (req, res) => {
  const { message, model } = req.body;
  try {
    const response = await axios.post('http://localhost:11434/api/generate', {
      model: 'minicpm-v',
      prompt: message,
      stream: false
    });
    res.json({ response: response.data.response });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Model processing error' });
  }
});

app.get('/api/models', async (req, res) => {
  try {
    const response = await axios.get(`${OLLAMA_URL}/api/tags`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch models' });
  }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, '0.0.0.0', () => console.log(`Server running on port ${PORT}`));