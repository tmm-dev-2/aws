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

app.use(cors());
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

app.post('/api/chat', async (req, res) => {
  const { message, model } = req.body;
  const modelConfig = MODEL_CONFIGS[model] || { temperature: 0.7, top_p: 0.9 };

  try {
    const response = await axios.post(`${OLLAMA_URL}/api/generate`, {
      model: model,
      prompt: message,
      stream: false,
      options: modelConfig
    });
    res.json({ response: response.data.response });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: `Model processing error: ${error.message}` });
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

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
