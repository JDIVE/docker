# Home Assistant Docker Setup

This directory contains configuration files for running Home Assistant in Docker.

## Directory Structure

- `docker-compose.yaml` - Docker Compose configuration file for Home Assistant
- `.gitignore` - Excludes sensitive data and runtime files from git
- `config-template/` - Template configuration files for reference
  - `configuration.yaml` - Main configuration file
  - `automations.yaml` - Automation definitions
  - `scripts.yaml` - Script definitions
  - `scenes.yaml` - Scene definitions

## Setup Instructions

1. Create a `config` directory if it doesn't exist
2. Copy the files from `config-template` to `config`
3. Start the container using Docker Compose:

```bash
docker-compose up -d
```

## Backup

Home Assistant has a built-in backup system that can be accessed via the UI at:
Settings > System > Backups

For more information, see the [Home Assistant Backup Documentation](https://www.home-assistant.io/integrations/backup/). 