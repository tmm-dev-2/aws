FROM ollama/ollama

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0:7860
ENV OLLAMA_ORIGINS=*
ENV HOME=/data

# Create data directory with proper permissions
WORKDIR /data
RUN mkdir -p .ollama && \
    chmod -R 777 . && \
    chown -R 1000:1000 .

USER 1000

# Create startup script
RUN echo '#!/bin/bash\n\
ollama serve --path /data/.ollama &\n\
sleep 10\n\
echo "Initializing Ollama..."\n\
ollama pull minicpm-v\n\
tail -f /dev/null' > start.sh && \
    chmod +x start.sh

EXPOSE 7860
CMD ["./start.sh"]