FROM ollama/ollama

# Start Ollama service and pull models
RUN ollama serve & \
    sleep 5 && \
    ollama pull mxbai-embed-large && \
    ollama pull minicpm-v && \
    ollama pull qwen2.5-coder && \
    ollama pull codegemma && \
    ollama pull codellama && \
    ollama pull llama3.2-vision

EXPOSE 11434
CMD ["serve"]
