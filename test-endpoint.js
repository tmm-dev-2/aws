import axios from 'axios';

const testEndpoint = async () => {
  try {
    const response = await axios.post('https://aide-project-1.onrender.com/api/chat', {
      message: 'hello',
      model: 'minicpm-v'
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    console.log('Response:', response.data);
  } catch (error) {
    console.log('Status:', error.response?.status);
    console.log('Headers:', error.response?.headers);
  }
};

testEndpoint();
