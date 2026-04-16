#!/bin/bash

# Setup script for Dingo OS development environment

echo "=== Dingo OS Setup ==="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Error: This script must run on Linux"
    exit 1
fi

echo "1. Checking dependencies..."

# Function to check if command exists
check_cmd() {
    if ! command -v $1 &> /dev/null; then
        echo "  ✗ $1 not found. Installing..."
        return 1
    else
        echo "  ✓ $1 found"
        return 0
    fi
}

# Check all dependencies
check_cmd "g++" || sudo apt install -y build-essential
check_cmd "make" || sudo apt install -y make
check_cmd "git" || sudo apt install -y git
check_cmd "python3" || sudo apt install -y python3

echo ""
echo "2. Creating directory structure..."
mkdir -p build/{bin,iso}
mkdir -p docs
mkdir -p tests
mkdir -p scripts
echo "  ✓ Directories created"

echo ""
echo "3. Making scripts executable..."
chmod +x src/showip/showip.sh
chmod +x scripts/*.sh 2>/dev/null
echo "  ✓ Scripts executable"

echo ""
echo "4. Building Task Manager..."
cd src/task-manager
make clean
make
if [[ $? -eq 0 ]]; then
    echo "  ✓ Task Manager built successfully"
else
    echo "  ✗ Task Manager build failed"
    exit 1
fi

cd ../..

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Test Task Manager: ./build/bin/task-manager"
echo "  2. Test showip: ./src/showip/showip.sh"
echo "  3. Install: make install"
echo ""
