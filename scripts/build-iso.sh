#!/bin/bash
# Dingo OS - ISO Build Script
# Generates bootable ISO using Cubic

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "╔════════════════════════════════════════╗"
echo "║  Dingo OS - ISO Builder (via Cubic)    ║"
echo "╚════════════════════════════════════════╝"

# Check if Cubic is installed
if ! command -v cubic &> /dev/null; then
    echo "❌ Cubic is not installed!"
    echo ""
    echo "Install Cubic with:"
    echo "  sudo apt install cubic"
    echo ""
    echo "Or download from: https://launchpad.net/cubic"
    exit 1
fi

echo "✓ Cubic found: $(cubic --version 2>/dev/null || echo 'installed')"

# Ensure build directories exist
mkdir -p build/iso
mkdir -p build/bin

# Build Task Manager if not already built
if [ ! -f build/bin/task-manager ]; then
    echo ""
    echo "Building Task Manager..."
    cd src/task-manager
    make clean
    make
    cd ../../
fi

echo "✓ Task Manager ready at: build/bin/task-manager"

# Check if showip is executable
if [ ! -x src/showip/showip.sh ]; then
    chmod +x src/showip/showip.sh
fi

echo "✓ showip ready at: src/showip/showip.sh"

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  Ready to Create ISO with Cubic        ║"
echo "╚════════════════════════════════════════╝"

echo ""
echo "Configuration files prepared:"
echo "  • cubic-config/preseed.cfg"
echo "  • cubic-config/custom-packages.list"
echo "  • cubic-config/custom-tasks.sh"

echo ""
echo "Utilities ready to include:"
echo "  • build/bin/task-manager (C++ binary)"
echo "  • src/showip/showip.sh (Bash script)"

echo ""
echo "Next steps:"
echo "1. Open Cubic GUI:"
echo "   sudo cubic"
echo ""
echo "2. In Cubic:"
echo "   • Select Ubuntu 22.04 LTS as base image"
echo "   • Copy utilities to: /root/Custom-Disk/usr/local/bin/"
echo "   • Apply preseed configuration"
echo "   • Add custom packages from custom-packages.list"
echo "   • Run custom-tasks.sh in terminal"
echo "   • Generate ISO"
echo ""
echo "3. Output will be: build/iso/dingo-os.iso"
echo ""
