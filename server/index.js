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

// Model-specific configurations
const MODEL_CONFIGS = {
  'mxbai-embed-large': { temperature: 0.8, top_p: 0.9 },
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

const OLLAMA_URL = 'http://localhost:7860';  // This becomes internal to the container
  app.get('/', async (req, res) => {
    const { logs, message } = req.query;
  
    if (logs === 'chat' && message) {
      try {
        const modelResponse = await axios.post(`/api/generate`, {
          model: 'minicpm-v',
          prompt: message,
          stream: false
        });
      
        // Send the actual model response
        res.send(modelResponse.data.response);
      } catch (error) {
        console.error('Model error:', error);
        // Send error message if model fails
        res.send("Model is processing, please try again");
      }
    } else if (logs === 'build') {
      res.send("Ollama is running");
    }
  });
// Update the chat endpoin`
app.post('/api/chat', async (req, res) => {
  const { message } = req.body;
  try {
    const response = await axios.post(`${OLLAMA_URL}/api/generate`, {
      model: 'minicpm-v',
      prompt: message,
      stream: false,
      options: {
        num_ctx: 2048,
        num_thread: 4
      }
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

const PORT = process.env.PORT || 7860;
app.listen(PORT, '0.0.0.0', () => console.log(`Server running on port ${PORT}`));