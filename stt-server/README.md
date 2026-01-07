# STT Server

NVIDIA NeMo-based speech-to-text server running on Tesla P4.

## Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set a secure API key:
   ```bash
   # Generate a random key
   openssl rand -hex 32
   ```

3. Start the service:
   ```bash
   docker compose up -d
   ```

## Configuration

- **docker-compose.yaml** - Service definition with Traefik labels
- **config/config.yaml** - Custom vocabulary and LLM cleanup rules
- **.env** - API key and model settings (not committed)

## Endpoints

| Endpoint | Auth | Purpose |
|----------|------|---------|
| `GET /health` | No | Liveness check |
| `GET /ready` | No | Readiness (models loaded) |
| `POST /transcribe` | Bearer token | Transcription |

## Notes

- Image must be transferred manually (90GB NeMo base image)
- First start downloads ~2GB of models to the volume
- LLM cleanup via Ollama is available but currently disabled (small models lack precision)
- NeMo's built-in punctuation model handles capitalisation and formatting
