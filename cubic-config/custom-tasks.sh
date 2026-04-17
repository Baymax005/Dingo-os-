#!/bin/bash
# Dingo OS - Post-installation setup script for Cubic
# This script runs after Ubuntu installation to customize the system

set -e

echo "=== Dingo OS Custom Setup ==="

# Create dingo user directories if needed
mkdir -p /home/dingo/.dingo
mkdir -p /usr/local/bin

echo "✓ Directories created"

# Make utilities executable
if [ -f /usr/local/bin/task-manager ]; then
    chmod +x /usr/local/bin/task-manager
    echo "✓ task-manager executable"
fi

if [ -f /usr/local/bin/showip ]; then
    chmod +x /usr/local/bin/showip
    echo "✓ showip executable"
fi

# Create a welcome message
cat > /etc/motd << 'EOF'
╔════════════════════════════════════════╗
║      Welcome to Dingo OS               ║
║  Custom Ubuntu with Task Manager       ║
║  and Network Utilities                 ║
╚════════════════════════════════════════╝

Available commands:
  • task-manager    - Process monitoring and control
  • showip          - Network interface information
  • ding            - Package manager wrapper

Try: task-manager --help
     showip --help

EOF

echo "✓ Welcome message installed"

# Set permissions for config files
if [ -d /etc/dingo ]; then
    chmod 755 /etc/dingo
    echo "✓ Config directory permissions set"
fi

echo "=== Setup Complete ==="
