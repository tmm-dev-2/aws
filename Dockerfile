FROM ollama/ollama

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0:7860
ENV OLLAMA_ORIGINS=*
ENV HOME=/app

# Create app directory with proper permissions
WORKDIR /app
RUN mkdir -p .ollama && \
    chmod -R 777 .ollama && \
    chown -R 1000:1000 .ollama

USER 1000

# Create startup script
RUN echo '#!/bin/bash\n\
ollama serve --path /app/.ollama &\n\
sleep 10\n\
echo "Initializing Ollama..."\n\
ollama pull minicpm-v\n\
tail -f /dev/null' > start.sh && \
    chmod +x start.sh

EXPOSE 7860
CMD ["./start.sh"]

#git add Dockerfile
#git commit -m "Update Dockerfile with Ollama service initialization"
#git push origin master