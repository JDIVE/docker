# Home Lab Docker Infrastructure

This repository contains the Docker infrastructure for a self-hosted home lab environment, providing various services through a secure and organized setup.

## Services Overview

### Traefik (Reverse Proxy)
- Main reverse proxy handling all incoming traffic
- Automatic SSL certificate management through Let's Encrypt
- Integration with Cloudflare DNS for domain validation
- Secure dashboard for monitoring and management

### GitLab
- Self-hosted Git repository management
- CI/CD pipelines
- Container registry
- Issue tracking and project management

### Homepage
- Customizable dashboard for your home lab
- Service status monitoring
- Bookmarks and quick access to services
- Widget support for extended functionality

### Nginx Proxy Manager (Legacy)
- Web UI for proxy management
- SSL certificate management
- Currently being migrated to Traefik

### Ollama
- Self-hosted AI model server
- Local AI model inference
- API access for integration with other services

## Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Domain name with Cloudflare DNS management
- Basic understanding of networking and Docker concepts

### Initial Setup

1. Clone this repository to your server:
   ```bash
   git clone <repository-url>
   cd docker
   ```

2. Set up environment files:
   ```bash
   # For Traefik
   cp traefik/.env.example traefik/.env
   # Edit the .env file with your specific configurations
   ```

3. Create required networks:
   ```bash
   docker network create proxy
   ```

4. Set up SSL certificates:
   - Ensure your domain is configured in Cloudflare
   - Update Cloudflare API tokens in the environment files
   - Traefik will automatically handle certificate generation

5. Start the core infrastructure:
   ```bash
   # Start Traefik first
   cd traefik
   docker-compose up -d

   # Then start other services as needed
   cd ../gitlab
   docker-compose up -d

   cd ../homepage
   docker-compose up -d
   ```

## Configuration

### Traefik
- Main configuration: `traefik/config/traefik.yaml`
- Service rules: `traefik/config/config.yaml`
- Environment variables: `traefik/.env`

Key features:
- Automatic SSL certificate generation and renewal
- Docker service discovery
- Secure dashboard access
- HTTP to HTTPS redirection

### GitLab
- Main configuration: `gitlab/config/gitlab.rb`
- Secrets: `gitlab/config/gitlab-secrets.json`
- Custom SSL certificates: `gitlab/config/ssl/`

### Homepage
- Service configuration: `homepage/data/services.yaml`
- Custom styling: `homepage/data/custom.css`
- Widgets: `homepage/data/widgets.yaml`

## Backup and Maintenance

### Data Persistence
All important data is stored in Docker volumes or bind-mounted directories:
- GitLab data: `gitlab/data/`
- Homepage configurations: `homepage/data/`
- SSL certificates: Managed by Traefik in `traefik/data/acme.json`

### Backup Recommendations
1. Regular backups of the `data/` directories
2. Export of GitLab settings and repositories
3. Backup of environment files
4. Regular monitoring of disk usage and system resources

## Security Considerations

1. All services are protected behind Traefik's reverse proxy
2. SSL/TLS encryption for all services
3. Regular updates of containers and base images
4. Secure storage of credentials in .env files (not in git)
5. Limited exposure of ports to host network

## Monitoring and Maintenance

1. Use Traefik's dashboard to monitor:
   - Service health
   - Certificate status
   - Traffic patterns

2. Regular tasks:
   - Check container logs for issues
   - Update container images
   - Verify backup integrity
   - Monitor disk usage
   - Review security policies

## Troubleshooting

Common issues and solutions:

1. Certificate Issues:
   - Verify Cloudflare API credentials
   - Check DNS propagation
   - Verify domain ownership

2. Network Issues:
   - Check Docker network connectivity
   - Verify port mappings
   - Review Traefik logs

3. Service Issues:
   - Check container logs
   - Verify environment variables
   - Check disk space and resource usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
