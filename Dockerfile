FROM ollama/ollama

# Create a startup script
RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 10\n\
ollama pull mxbai-embed-large\n\
ollama pull minicpm-v\n\
ollama pull qwen2.5-coder\n\
ollama pull codegemma\n\
ollama pull codellama\n\
ollama pull llama3.2-vision\n\
wait' > /start.sh && chmod +x /start.sh

EXPOSE 11434
CMD ["/start.sh"]
