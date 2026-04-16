# Dingo OS - Quick Start Checklist

**Status: Ready for Ubuntu VM setup**

## When Ubuntu is Installed (Do This)

### 1. Copy This Project to VM
```bash
# On your Windows machine, use file explorer or scp to copy:
# C:\Users\muham\OneDrive\Desktop\OTHER LANGS\OS project\
# into your Ubuntu VM home directory as ~/Dingo-OS
```

### 2. Run Setup in VM Terminal
```bash
cd ~/Dingo-OS
bash scripts/setup.sh
```

This will:
- ✓ Install all dependencies (g++, make, git)
- ✓ Create necessary directories
- ✓ Build Task Manager from C++ source
- ✓ Prepare showip script

### 3. Test Both Utilities

**Task Manager:**
```bash
# View all processes
./build/bin/task-manager

# Show help
./build/bin/task-manager --help

# Try to kill a process (with confirmation)
./build/bin/task-manager --kill $(pgrep -f 'sleep' | head -1)
```

**showip:**
```bash
# Show all network interfaces
./src/showip/showip.sh

# Show specific interface
./src/showip/showip.sh lo

# Show help
./src/showip/showip.sh --help
```

### 4. Optional: Install to System
```bash
make install

# Now you can run from anywhere:
task-manager
showip
```

---

## What's Ready to Go

| Component | Status | Location |
|-----------|--------|----------|
| Task Manager (C++) | ✓ Complete | `src/task-manager/src/` |
| showip (Bash) | ✓ Complete | `src/showip/showip.sh` |
| Makefile system | ✓ Complete | `Makefile`, `src/task-manager/Makefile` |
| Setup script | ✓ Complete | `scripts/setup.sh` |
| Documentation | ✓ Complete | `README.md`, `PROPOSAL.md`, `ARCHITECTURE.md` |

---

## Next Phase: ISO Integration (Once Utilities Work)

Once testing passes, we'll:
1. Use Cubic to create bootable ISO
2. Include Task Manager + showip
3. Test boot on VM
4. Demo for submission

---

## Troubleshooting

**Compilation error?**
```bash
cd src/task-manager
make clean
make
```

**Permission denied?**
```bash
chmod +x scripts/*.sh
chmod +x src/showip/showip.sh
```

**Dependencies not installed?**
```bash
sudo apt install build-essential g++ make git
```

---

**Once Ubuntu is ready, just run `bash scripts/setup.sh` and let me know if there are any issues!**
