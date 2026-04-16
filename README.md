# Dingo OS - Build & Run Guide

## Quick Start (Ubuntu VM)

### 1. Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git g++ gcc make cmake python3 python3-pip cubic
```

### 2. Navigate to Project
```bash
cd ~/Dingo-OS  # or wherever you cloned the repo
```

### 3. Build Task Manager
```bash
cd src/task-manager
make clean
make
```

This compiles the C++ code and outputs to `build/bin/task-manager`

### 4. Make showip Executable
```bash
chmod +x src/showip/showip.sh
```

### 5. Test the Utilities

**Test Task Manager:**
```bash
# List all processes
./build/bin/task-manager

# Filter by name (e.g., bash processes)
./build/bin/task-manager --filter bash

# Kill a process (with confirmation)
./build/bin/task-manager --kill <PID>
```

**Test showip:**
```bash
./src/showip/showip.sh

# Show specific interface
./src/showip/showip.sh eth0
```

### 6. Install to System PATH (Optional)
```bash
sudo cp build/bin/task-manager /usr/local/bin/
sudo cp src/showip/showip.sh /usr/local/bin/showip
sudo chmod +x /usr/local/bin/showip

# Now you can run from anywhere:
task-manager
showip
```

---

## Project Structure

```
Dingo-OS/
├── src/
│   ├── task-manager/          # C++ process manager
│   │   ├── src/
│   │   │   ├── main.cpp
│   │   │   ├── process.cpp
│   │   │   ├── process.h
│   │   │   └── Makefile
│   │   └── ...
│   └── showip/                # Network utilities
│       └── showip.sh
├── build/
│   └── bin/                   # Compiled binaries go here
├── docs/
└── PROPOSAL.md
└── ARCHITECTURE.md
```

---

## Next Steps: ISO Integration with Cubic

Once both utilities are working, we'll integrate them into a bootable ISO using Cubic:

1. **Launch Cubic GUI:**
   ```bash
   sudo cubic
   ```

2. **Select Ubuntu 22.04 LTS ISO**

3. **Copy utilities into Cubic's include list**

4. **Build ISO**

5. **Test boot in VM**

---

## Troubleshooting

### Task Manager won't compile?
- Make sure you have `g++` and `make` installed: `sudo apt install build-essential`
- Check that the source files are in `src/task-manager/src/`

### Task Manager shows no processes?
- Run with `sudo`: `sudo ./build/bin/task-manager`
- Check that `/proc` filesystem is available

### showip not running?
- Make sure it's executable: `chmod +x src/showip/showip.sh`
- Test with: `bash src/showip/showip.sh`

---

## Files Ready to Copy-Paste

All source files are prepared in this repo. You just need to:
1. Copy the entire folder structure to your Ubuntu VM
2. Follow the "Quick Start" section above
