FROM python:3.9-slim

WORKDIR /app

# Install litellm
RUN pip install litellm[proxy]

# Copy configuration
COPY ./data/config.yaml /app/config.yaml

# Set environment variables
ENV PORT=8000
ENV HOST=0.0.0.0

# Run the proxy server
CMD ["litellm", "--config", "/app/config.yaml"] 