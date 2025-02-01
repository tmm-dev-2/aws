FROM ollama/ollama

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0:7860
ENV OLLAMA_ORIGINS=*

# Create directories with proper permissions
RUN mkdir -p /data/.ollama && \
    chmod -R 777 /data/.ollama && \
    ln -sf /data/.ollama /.ollama

# Create startup script with explicit path and initialization
RUN echo '#!/bin/bash\n\
ollama serve --path /data/.ollama &\n\
sleep 10\n\
echo "Initializing Ollama..."\n\
ollama pull minicpm-v\n\
tail -f /dev/null' > /start.sh && \
    chmod +x /start.sh

EXPOSE 7860
CMD ["/start.sh"]

#git add Dockerfile
#git commit -m "Update Dockerfile with Ollama service initialization"
#git push origin master