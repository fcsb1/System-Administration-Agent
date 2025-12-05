#!/bin/bash
# Start Ollama in background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
sleep 5

# Pull the model
ollama pull qwen3:14b

# Stop Ollama
kill $OLLAMA_PID