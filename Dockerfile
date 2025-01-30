FROM ollama/ollama

# Create a startup script with environment variable for port
RUN echo '#!/bin/bash\n\
export OLLAMA_HOST=0.0.0.0:10000\n\
ollama serve &\n\
sleep 20\n\
for model in mxbai-embed-large minicpm-v qwen2.5-coder codegemma codellama llama3.2-vision; do\n\
  echo "Pulling $model..."\n\
  ollama pull $model\n\
  sleep 5\n\
done\n\
wait' > /start.sh && chmod +x /start.sh

EXPOSE 10000
ENTRYPOINT ["/bin/bash", "/start.sh"]

#git add Dockerfile
#git commit -m "Update Dockerfile with Ollama service initialization"
#git push origin master