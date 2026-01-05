# Installation

This guide covers how to install OpenPLC Runtime v4 on Linux systems.

## Prerequisites

- Linux operating system (Ubuntu 20.04+, Debian 11+, or equivalent)
- Root or sudo access
- Git installed
- Internet connection for downloading dependencies

## Native Linux Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Autonomy-Logic/openplc-runtime.git
cd openplc-runtime
```

### Step 2: Run the Installation Script

```bash
sudo ./install.sh
```

The installation script automatically:

- Detects your Linux distribution
- Installs all required dependencies
- Creates Python virtual environments
- Compiles the runtime
- Sets up system services

### Step 3: Start the Runtime

```bash
sudo ./start_openplc.sh
```

Once started, the runtime listens on port 8443 for connections from OpenPLC Editor.

## Docker Installation

### Linux Docker

```bash
docker pull autonomylogic/openplc-runtime:latest
docker run -d -p 8443:8443 autonomylogic/openplc-runtime:latest
```

### macOS Docker

Since OpenPLC Runtime requires Linux, macOS users can run it in Docker:

```bash
docker pull autonomylogic/openplc-runtime:latest
docker run -d -p 8443:8443 autonomylogic/openplc-runtime:latest
```

## Verifying Installation

After installation, verify the runtime is running:

1. Check the service status:
   ```bash
   systemctl status openplc
   ```

2. Test the API endpoint:
   ```bash
   curl -k https://localhost:8443/api/health
   ```

3. Connect from OpenPLC Editor to complete setup

## First-Time Setup

After installation, you need to create the first user account. See [First User Setup](first-user-setup.md) for instructions.

## Updating the Runtime

To update to a newer version:

```bash
cd openplc-runtime
git pull
sudo ./install.sh
sudo systemctl restart openplc
```

## Troubleshooting

### Installation Fails

1. Check that you have sudo privileges
2. Ensure all prerequisites are installed
3. Check the installation log for specific errors

### Runtime Won't Start

1. Check for port conflicts on 8443
2. Review system logs: `journalctl -u openplc`
3. Verify all dependencies were installed

### Cannot Connect from Editor

1. Verify the runtime is running
2. Check firewall settings for port 8443
3. Ensure you're using HTTPS (not HTTP)
