FROM ollama/ollama

# Set up permissions and directories
USER root
RUN mkdir -p /ollama && \
    chmod -R 777 /ollama && \
    ln -s /ollama /.ollama

ENV OLLAMA_HOME=/ollama
ENV OLLAMA_HOST=0.0.0.0:7860

RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 10\n\
echo "Starting Ollama service..."\n\
echo "Pulling minicpm-v..."\n\
ollama pull minicpm-v\n\
wait' > /start.sh && chmod +x /start.sh

EXPOSE 7860
CMD ["/bin/bash", "/start.sh"]

#git add Dockerfile
#git commit -m "Update Dockerfile with Ollama service initialization"
#git push origin master