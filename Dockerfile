FROM ollama/ollama

# Set up proper permissions
USER root
RUN mkdir -p /home/ollama/.ollama && \
    chown -R 1000:1000 /home/ollama

# Switch to non-root user
USER 1000

RUN echo '#!/bin/bash\n\
export OLLAMA_HOME=/home/ollama/.ollama\n\
export OLLAMA_HOST=0.0.0.0:7860\n\
ollama serve &\n\
sleep 20\n\
echo "Pulling minicpm-v..."\n\
ollama pull minicpm-v\n\
wait' > /start.sh && chmod +x /start.sh

EXPOSE 7860
ENTRYPOINT ["/bin/bash", "/start.sh"]

#git add Dockerfile
#git commit -m "Update Dockerfile with Ollama service initialization"
#git push origin master