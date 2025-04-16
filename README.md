# Home Lab Docker Infrastructure

## Services Overview

### Core Infrastructure

#### Traefik (Reverse Proxy)
- Main reverse proxy handling all incoming traffic
- Automatic SSL certificate management through Let's Encrypt
- Integration with Cloudflare DNS for domain validation
- Secure dashboard for monitoring and management
- HTTP to HTTPS redirection

#### Homepage
- Customizable dashboard for your home lab
- Service status monitoring
- Bookmarks and quick access to services
- Widget support for extended functionality
- Docker integration for container status

#### Uptime Kuma
- Service monitoring and status page
- Real-time uptime checks (HTTP, Ping, Port, etc.)
- Notification integrations (Email, Slack, Discord, etc.)
- Customizable status pages

### Development & Administration

#### GitLab
- Self-hosted Git repository management
- CI/CD pipelines
- Container registry
- Issue tracking and project management

#### Nginx Proxy Manager (Legacy)
- Web UI for proxy management
- SSL certificate management
- Currently being migrated to Traefik

### Systems Management

#### Proxmox (External)
- Virtualization platform
- VM and container management
- Accessed via Traefik reverse proxy

#### TrueNAS (External)
- Network Attached Storage
- ZFS-based storage system
- Accessed via Traefik reverse proxy

#### UniFi Controller (External)
- Network management
- Device monitoring
- Accessed via Traefik reverse proxy

### Media & Home Services

#### Jellyfin
- Media server for movies, TV, music, and photos
- User management with profiles
- Transcoding capabilities
- Mobile apps available

#### Mealie
- Recipe management and meal planning
- Automatic recipe import from websites
- Shopping list generation
- Meal calendar for planning
- Mobile-friendly interface

#### Home Assistant
- Home automation platform
- IoT device integration and control
- Automation workflows
- Energy monitoring
- Accessed via Traefik reverse proxy

### AI & Development

#### Ollama
- Self-hosted AI model server
- Local AI model inference
- API access for integration with other services

#### Open WebUI
- Web interface for Ollama AI models
- Provides a user-friendly chat interface
- Manages models and configurations

#### LiteLLM
- LLM API Gateway and Router
- Standardizes API calls to various LLMs
- Provides load balancing and fallback options

#### n8n
- Workflow automation platform
- Connects different services and APIs
- Visual workflow editor

### Productivity & Utilities

#### Linkwarden
- Self-hosted collaborative bookmark manager
- Preserves web pages as snapshots (HTML, PDF, Screenshot)
- Organize links with collections and tags
- Accessed via Traefik reverse proxy

#### AppFlowy
- Open-source alternative to Notion
- Knowledge base and note-taking application
- Document management with rich text editor
- Tasks and kanban boards
- Accessed via Traefik reverse proxy

## Installation Guide

### Prerequisites
- Linux server with Docker (20.10+) and Docker Compose (v2+) installed
- Domain name with Cloudflare DNS management
- SSL/TLS certificates from Let's Encrypt (managed automatically by Traefik)
- Basic understanding of networking and Docker concepts
- Port 80 and 443 accessible from the internet
- For Jellyfin: sufficient storage for media files

### Detailed Setup Instructions

#### 1. System Preparation

Install Docker and Docker Compose if not already installed:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add your user to the docker group
sudo usermod -aG docker $USER

# Apply changes (or log out and back in)
newgrp docker
```

#### 2. Repository Setup

Clone the repository to your server:
```bash
git clone <repository-url>
cd docker
```

#### 3. Network Setup

Create the required Docker network for all services:
```bash
docker network create proxy
```

#### 4. Environment Configuration

Set up environment files for each service:

```bash
# Create and configure Traefik environment file
cp traefik/.env.example traefik/.env

# Create and configure Linkwarden environment file (requires manual password entry)
# (The NEXTAUTH_SECRET will be generated if not present)
cp linkwarden/.env.example linkwarden/.env # Or create manually if no example
```

Edit the `.env` files with your specific configurations:

```bash
# Example configurations for traefik/.env
TRAEFIK_DASHBOARD_AUTH=admin:$(htpasswd -nb admin your_secure_password | sed 's/\\$/\\$\\$/g')
TRAEFIK_ACME_EMAIL=your.email@example.com
TRAEFIK_LOG_PATH=/var/log/traefik/access.log
CF_DNS_API_TOKEN=your_cloudflare_api_token_here
DOMAIN_TRAEFIK=traefik.openshaw.tech
DOMAIN_GITLAB=gitlab.openshaw.tech
# Add other domain names as needed

# Example structure for linkwarden/.env (Set SECURE passwords!)
# NEXTAUTH_SECRET=YOUR_SECURE_NEXTAUTH_SECRET_HERE
# NEXTAUTH_URL=https://linkwarden.openshaw.tech/api/v1/auth
# POSTGRES_USER=linkwarden
# POSTGRES_PASSWORD=YOUR_SECURE_POSTGRES_PASSWORD_HERE
# POSTGRES_DB=linkwarden
```

#### 5. Directory Preparation

Prepare directories for persistent data and ensure proper permissions:

```bash
# Create required directories for Traefik
mkdir -p traefik/data
touch traefik/data/acme.json
chmod 600 traefik/data/acme.json

# Prepare directories for other services as needed
mkdir -p gitlab/{config,logs,data}
mkdir -p homepage/data
mkdir -p mealie/data
mkdir -p ollama/data
mkdir -p jellyfin/data
mkdir -p linkwarden # Added for Linkwarden volumes (pgdata, data)
mkdir -p uptime-kuma/data # Added for Uptime Kuma
```

#### 6. Cloudflare DNS Configuration

1. Login to your Cloudflare account
2. Add DNS records for each service:
   - Type: A or CNAME
   - Name: subdomain (e.g., traefik, gitlab, uptime)
   - Content: Your server's IP address
   - Proxy status: DNS only (gray cloud)

#### 7. Service Deployment

Deploy services in the correct order:

```bash
# Start Traefik first (core infrastructure)
cd traefik
docker compose up -d
cd ..

# Deploy Homepage dashboard
cd homepage
docker compose up -d
cd ..

# Deploy GitLab (may take several minutes to fully initialize)
cd gitlab
docker compose up -d
cd ..

# Deploy other services
cd ollama
docker compose up -d
cd ..

cd mealie
docker compose up -d
cd ..

# Deploy AppFlowy
cd appflowy
docker compose up -d
cd ..

cd jellyfin
docker compose up -d
cd ..

# Deploy Linkwarden
cd linkwarden
# IMPORTANT: Ensure .env has secrets before running!
docker compose up -d
cd ..

# Deploy Uptime Kuma
cd uptime-kuma
docker compose up -d
cd ..
```

#### 8. Home Assistant Setup

Refer to the `homeassistant` directory for detailed setup and configuration instructions.

```bash
# Start Home Assistant
cd homeassistant
docker compose up -d
cd ..
```

#### 9. Verify Deployments

Check that all containers are running correctly:
```bash
docker ps
```

Verify service access through your domain names:
- https://traefik.openshaw.tech
- https://gitlab.openshaw.tech
- https://homepage.openshaw.tech
- https://recipes.openshaw.tech
- https://jellyfin.openshaw.tech
- https://ollama.openshaw.tech
- https://linkwarden.openshaw.tech
- https://uptime.openshaw.tech

## Configuration Details

### Traefik Configuration
- **Main configuration**: `traefik/config/traefik.yaml`
  - Controls log levels, entry points, and global settings
  - Configures the dashboard and API access
  - Sets up certificate resolvers for Let's Encrypt
  - Defines Docker provider settings
  
- **Service rules**: `traefik/config/config.yaml`
  - Contains static service definitions for external services
  - Defines routing rules, middlewares, and load balancer options
  - Configures TLS settings for each service
  
- **Environment variables**: `traefik/.env`
  - Cloudflare API credentials for DNS challenges
  - Dashboard authentication credentials
  - Domain names for each service
  - Log file paths

**Key Features**:
- Automatic SSL certificate generation and renewal using Let's Encrypt
- DNS-01 challenge through Cloudflare for wildcard certificates
- Docker service discovery for automatic container registration
- Secure dashboard access with basic authentication
- HTTP to HTTPS redirection for all services
- Support for both Docker-based and external services

### GitLab Configuration
- **Main configuration**: `gitlab/config/gitlab.rb`
  - Server settings, feature toggles, and integration options
  - SMTP configuration for email notifications
  - Backup settings and scheduling
  
- **Secrets**: `gitlab/config/gitlab-secrets.json`
  - Automatically generated secrets for GitLab services
  - Should not be manually edited
  
- **Custom SSL certificates**: `gitlab/config/ssl/`
  - SSL certificates are managed by Traefik
  - GitLab is configured to use HTTP behind Traefik's SSL termination
  
- **Important settings**:
  - GitLab is exposed on ports 8929 (HTTP), 8930 (HTTPS), and 8922 (SSH)
  - Traefik routes traffic based on the hostname `gitlab.openshaw.tech`

### Homepage Configuration
- **Service configuration**: `homepage/data/services.yaml`
  - Defines service groups and their details
  - Sets icons, URLs, and descriptions for each service
  
- **Custom styling**: `homepage/data/custom.css`
  - Custom CSS for Homepage appearance
  
- **Widgets**: `homepage/data/widgets.yaml`
  - Configures dashboard widgets and their placement
  - Integrates with Docker for container status
  
- **Environment settings**:
  - Allowed hosts configuration: `HOMEPAGE_ALLOWED_HOSTS=10.1.10.10:3000,homepage.openshaw.tech`
  - Docker socket mounted for container integration

### Jellyfin Configuration
- **Docker Compose configuration**: `jellyfin/docker-compose.yaml`
  - Container environment variables for user/group IDs
  - Volume mappings for configuration and media
  - Optional GPU passthrough (currently commented out)
  
- **Media directories**: 
  - `/mnt/dozer/media` mapped to `/data` inside the container
  - Persistent volume for configuration data
  
- **Network settings**:
  - Discovery ports: 7359/udp and 1900/udp for DLNA
  - Traefik labels for routing through `jellyfin.openshaw.tech`

### Mealie Configuration
- **Docker Compose configuration**: `mealie/docker-compose.yaml`
  - Environment variables for feature toggles
  - Volume mappings for persistent data
  
- **Data storage**: `mealie/data/`
  - Database files
  - Recipe images and backups
  - User data and templates
  
- **Key settings**:
  - Recipe visibility: `RECIPE_PUBLIC=true`
  - Signup allowed: `ALLOW_SIGNUP=true`
  - Port 9000 exposed internally and routed through Traefik

### Ollama Configuration
- **Docker Compose configuration**: `ollama/docker-compose.yaml`
  - Volume mapping for model storage
  - Network configuration for API access
  - GPU configuration for hardware acceleration
  
- **Data storage**: `ollama_data` Docker volume
  - Stores downloaded AI models
  - Persists configuration between container restarts
  
- **API access**:
  - Internal port 11434 exposed for API calls
  - Accessible through Traefik at `ollama.openshaw.tech`

- **GPU Configuration**:
  - Uses NVIDIA runtime for GPU acceleration
  - Environment variables:
    - `NVIDIA_VISIBLE_DEVICES=all` - Makes all GPUs visible to the container
    - `NVIDIA_DRIVER_CAPABILITIES=compute,utility` - Enables necessary GPU functions
  - Memory limits:
    - Set to 40GB for larger language models
  - For large models (like Gemma3:27b), ensure:
    - Sufficient host RAM (minimum 32GB, recommended 48GB)
    - NVIDIA GPU with adequate VRAM (24GB+ for full-sized models)
    - VM configuration with proper VFIO passthrough (if using VMs)

### Linkwarden Configuration
- **Docker Compose configuration**: `linkwarden/docker-compose.yaml`
  - Environment variables for Linkwarden configuration
  - Volume mappings for Linkwarden data and configuration

### Uptime Kuma Configuration
- **Docker Compose configuration**: `uptime-kuma/docker-compose.yaml`
  - Volume mapping for persistent data (`./data:/app/data`)
  - Traefik labels for routing through `uptime.openshaw.tech`
- **Configuration**: Done via the web UI at `https://uptime.openshaw.tech` after initial setup.
- **Data storage**: `uptime-kuma/data/`
  - Stores monitor configurations, history, and user settings.

## Backup and Maintenance

### Automated Backup Strategy

#### GitLab
GitLab has built-in backup functionality:

```bash
# Enter the GitLab container
docker exec -it gitlab /bin/bash

# Create a backup
gitlab-backup create STRATEGY=copy

# Exit the container
exit

# Copy backups to a safe location
rsync -avz ~/docker/gitlab/data/backups/ /path/to/backup/destination/
```

#### Mealie
Mealie creates automatic database backups:
```bash
# Copy Mealie backups to external storage
rsync -avz ~/docker/mealie/data/backups/ /path/to/backup/destination/
```

#### Uptime Kuma
Uptime Kuma stores its configuration in a SQLite database within its data volume.
```bash
# Backup Uptime Kuma data volume
rsync -avz ~/docker/uptime-kuma/data/ /path/to/backup/destination/uptime-kuma-data/
```

#### Critical Configuration Files
Create a script to regularly backup your configuration files:

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backup/destination/configs-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup environment files
cp ~/docker/traefik/.env $BACKUP_DIR/traefik.env
cp ~/docker/*/.env $BACKUP_DIR/ 2>/dev/null

# Backup configuration files
cp -r ~/docker/traefik/config $BACKUP_DIR/traefik-config
cp -r ~/docker/homepage/data/*.yaml $BACKUP_DIR/homepage-config
cp -r ~/docker/gitlab/config/gitlab.rb $BACKUP_DIR/gitlab-config

# Backup SSL certificates
cp ~/docker/traefik/data/acme.json $BACKUP_DIR/

# Compress backup
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "Backup completed: $BACKUP_DIR.tar.gz"
```

Save this as `backup-configs.sh`, make it executable with `chmod +x backup-configs.sh` and schedule it with cron.

### Update and Maintenance Procedures

#### Container Updates
Regular update script:

```bash
#!/bin/bash
LOG_FILE="/var/log/docker-updates.log"
echo "Docker update started at $(date)" >> $LOG_FILE

cd ~/docker

# Update container images
echo "Pulling latest images..." >> $LOG_FILE
docker compose pull >> $LOG_FILE 2>&1

# Restart services with new images
services=("traefik" "gitlab" "homepage" "mealie" "ollama" "jellyfin" "linkwarden" "uptime-kuma")
for service in "${services[@]}"; do
  echo "Updating $service..." >> $LOG_FILE
  cd ~/docker/$service
  docker compose down
  docker compose up -d
  cd ~/docker
  echo "$service updated successfully." >> $LOG_FILE
done

echo "Docker update completed at $(date)" >> $LOG_FILE
```

Save this as `update-containers.sh`, make it executable and schedule it during a maintenance window.

#### System Maintenance Checklist
Perform these tasks monthly:

1. Check disk space usage:
   ```bash
   df -h
   docker system df
   ```

2. Clean up unused Docker resources:
   ```bash
   docker system prune --volumes
   ```

3. Check container logs for errors:
   ```bash
   for service in traefik gitlab homepage mealie ollama jellyfin linkwarden uptime-kuma; do
     docker logs --tail 100 $service > /tmp/$service-logs.txt
   done
   grep -i error /tmp/*-logs.txt
   ```

4. Verify SSL certificate expiration dates:
   ```bash
   # Check main domain
   echo | openssl s_client -servername traefik.openshaw.tech -connect traefik.openshaw.tech:443 2>/dev/null | openssl x509 -noout -dates
   # Check another service domain
   echo | openssl s_client -servername uptime.openshaw.tech -connect uptime.openshaw.tech:443 2>/dev/null | openssl x509 -noout -dates
   ```

5. Verify backup integrity:
   ```bash
   # Test restore a backup to a temporary location
   docker run --rm -v ~/docker/gitlab/data/backups:/backups -v /tmp/gitlab-restore:/restore gitlab/gitlab-ce bash -c "mkdir -p /restore && tar -xf /backups/latest-backup.tar -C /restore"
   ```

## Security Considerations

### Network Security
1. **Firewall Configuration**:
   ```bash
   # Allow only necessary ports
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow 22/tcp          # SSH
   sudo ufw allow 80/tcp          # HTTP
   sudo ufw allow 443/tcp         # HTTPS
   sudo ufw enable
   ```

2. **Traefik Security Headers**:
   Add to your Traefik configuration:
   ```yaml
   # Add to traefik.yaml
   middlewares:
     security-headers:
       headers:
         frameDeny: true
         browserXssFilter: true
         contentTypeNosniff: true
         forceSTSHeader: true
         stsIncludeSubdomains: true
         stsPreload: true
         stsSeconds: 31536000
   ```

3. **Container Security**:
   - Run containers as non-root users where possible
   - Use read-only file systems where applicable
   - Limit container capabilities

### Access Security
1. **Two-factor authentication**:
   - Enable 2FA for GitLab
   - Use strong passwords for all service dashboards

2. **Regular Credential Rotation**:
   - Change API keys quarterly
   - Update dashboard passwords regularly

3. **SSH Hardening**:
   ```bash
   # Edit SSH configuration
   sudo nano /etc/ssh/sshd_config
   
   # Recommended settings
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes
   ```

4. **Secrets Management**:
   - Store all credentials in .env files (excluded from git)
   - Consider using Docker secrets for production environments

## Monitoring

### Basic Monitoring Setup

1. **Uptime Kuma**:
   - Use the Uptime Kuma instance at `https://uptime.openshaw.tech` to monitor all other services.

2. **Traefik Access Logs**:
   - Review logs regularly: `cat ${TRAEFIK_LOG_PATH}`
   - Set up log rotation to prevent disk filling

3. **Docker Stats**:
   ```bash
   # Live container resource usage
   docker stats
   ```

4. **Advanced Monitoring**:
   Consider adding Prometheus and Grafana:
   ```yaml
   # Add to docker-compose.yaml
   prometheus:
     image: prom/prometheus
     volumes:
       - ./prometheus:/etc/prometheus
     # ...configuration...

   grafana:
     image: grafana/grafana
     # ...configuration...
   ```

## Troubleshooting Guide

### Certificate Issues

1. **Let's Encrypt Rate Limits**:
   - Problem: Too many certificate requests
   - Solution: Use staging environment first
     ```yaml
     # In traefik.yaml
     certificatesResolvers:
       letsencrypt:
         acme:
           caServer: "https://acme-staging-v02.api.letsencrypt.org/directory"
     ```

2. **Cloudflare DNS Verification**:
   - Problem: DNS-01 challenge failing
   - Solution: Verify API token permissions (Zone:DNS:Edit)
   - Check logs: `docker logs traefik`

3. **Certificate Renewal**:
   - Problem: Certificates not renewing
   - Solution: Check permissions on `acme.json` (chmod 600)
   - Verify Traefik can reach Let's Encrypt servers

### Network Issues

1. **Container Cannot Reach Internet**:
   - Problem: DNS resolution issues
   - Solution: Add DNS servers to Docker daemon
     ```json
     # /etc/docker/daemon.json
     {
       "dns": ["1.1.1.1", "8.8.8.8"]
     }
     ```
   - Restart Docker: `sudo systemctl restart docker`

2. **Services Can't Communicate**:
   - Problem: Containers can't reach each other
   - Solution: Verify all containers are on the `proxy` network
     ```bash
     docker network inspect proxy
     ```

3. **Port Conflicts**:
   - Problem: Services fail to start due to port conflicts
   - Solution: Check if ports are already in use
     ```bash
     sudo netstat -tulpn | grep LISTEN
     ```

### Service-Specific Issues

1. **GitLab Slow/Unresponsive**:
   - Problem: High resource usage
   - Solution: Adjust resource limits in `gitlab.rb`
     ```ruby
     # Reduce worker counts
     sidekiq['concurrency'] = 5
     puma['worker_processes'] = 2
     ```
   - Increase server resources if possible

2. **Jellyfin Transcoding Issues**:
   - Problem: Videos stutter or fail to play
   - Solution: Enable hardware acceleration
     ```yaml
     # Uncomment in docker-compose.yaml
     deploy:
       resources:
         reservations:
           devices:
             - driver: nvidia
               count: 1
               capabilities: [gpu]
     ```
   - Install appropriate GPU drivers on host

3. **Traefik Dashboard 404**:
   - Problem: Can't access Traefik dashboard
   - Solution: Verify API is enabled and dashboard middleware
     ```yaml
     # traefik.yaml
     api:
       dashboard: true
     ```

## Advanced Topics

### Adding New Services

To add a new service to your infrastructure:

1. Create a new directory in `~/docker/`
2. Create a `docker-compose.yaml` file with appropriate Traefik labels:
   ```yaml
   services:
     new-service:
       image: new-service-image
       container_name: new-service
       labels:
         - "traefik.enable=true"
         - "traefik.http.routers.new-service.rule=Host(`new-service.openshaw.tech`)"
         - "traefik.http.routers.new-service.entrypoints=websecure"
         - "traefik.http.routers.new-service.tls.certresolver=letsencrypt"
         - "traefik.http.services.new-service.loadbalancer.server.port=SERVICE_PORT"
         # Example for Uptime Kuma:
         # - "traefik.http.routers.uptime-kuma.rule=Host(`uptime.openshaw.tech`)"
         # - "traefik.http.services.uptime-kuma.loadbalancer.server.port=3001"
       networks:
         - proxy
   
   networks:
     proxy:
       external: true
   ```

3. Add the service to Homepage dashboard in `homepage/data/services.yaml`
4. Add the service to Uptime Kuma for monitoring via its web UI.
5. Deploy the service: `docker compose up -d`

### Implementing High Availability

For critical services, consider implementing high availability:

1. Use Docker Swarm or Kubernetes for container orchestration
2. Implement database replication for stateful services
3. Use shared storage solutions for persistent data
4. Configure load balancing across multiple nodes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## AppFlowy Setup with Traefik

AppFlowy requires special configuration to work with Traefik reverse proxy. The default Docker Compose configuration assumes direct access to the AppFlowy services, but with Traefik, we need to add an intermediary nginx container to handle routing.

### Key Modifications for Traefik Integration

1. **Added nginx as an intermediate service**:
   - Created a custom nginx.conf file that routes traffic appropriately between Traefik and AppFlowy's services
   - The nginx container connects to both the internal AppFlowy network and the Traefik proxy network
   - All internal services remain on the default network, isolated from direct external access

2. **Environment Variable Updates**:
   - Ensured that `AF_BASE_URL` and `APPFLOWY_WEB_URL` point to the correct external domain
   - Added `AF_GOTRUE_URL` to properly configure authentication endpoints
   - Changed `SCHEME` from http to https for secure communication

3. **Traefik Labels**:
   - Added only to the nginx container, which serves as the single entry point from Traefik
   - All internal routing is handled by nginx's configuration

### Nginx Configuration

The nginx.conf file contains routing rules for:
- GoTrue authentication service (/gotrue/)
- WebSocket connections (/event)
- REST API endpoints (/api)
- Admin Console (/console)
- MinIO storage (/minio and /minio-api)
- Root web application (/)

This approach simplifies the Traefik configuration while maintaining the expected routing structure for AppFlowy's services.
