FROM ollama/ollama

WORKDIR /app

# Create necessary directories with correct permissions
RUN mkdir -p /root/.ollama && \
    chmod -R 777 /root/.ollama

ENV OLLAMA_HOST=0.0.0.0:7860
ENV HOME=/root

# Create and configure startup script
COPY <<EOF /app/start.sh
#!/bin/bash
ollama serve &
sleep 15
echo "Starting Ollama service..."
echo "Pulling minicpm-v..."
ollama pull minicpm-v
tail -f /dev/null
EOF

RUN chmod +x /app/start.sh

EXPOSE 7860
CMD ["/app/start.sh"]
#git add Dockerfile
#git commit -m "Update Dockerfile with Ollama service initialization"
#git push origin master