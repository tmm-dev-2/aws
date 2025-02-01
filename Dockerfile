FROM ollama/ollama

VOLUME /root/.ollama

# Create a startup script with single lightweight model
RUN echo '#!/bin/bash\n\
export OLLAMA_HOST=0.0.0.0:10000\n\
ollama serve &\n\
sleep 20\n\
echo "Pulling minicpm-v..."\n\
ollama pull minicpm-v\n\
wait' > /start.sh && chmod +x /start.sh

EXPOSE 10000
ENTRYPOINT ["/bin/bash", "/start.sh"]


#git add Dockerfile
#git commit -m "Update Dockerfile with Ollama service initialization"
#git push origin master