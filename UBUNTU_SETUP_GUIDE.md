# Dingo OS - Ubuntu VM Setup Guide (Step-by-Step)

**Status**: Code is pushed to GitHub ✅  
**Next**: Follow these steps in your Ubuntu VM

---

## Step 1: Initial Ubuntu Setup (5 minutes)

Once Ubuntu 22.04 is running, open a terminal and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required tools
sudo apt install -y build-essential g++ gcc make git python3 python3-pip
```

**Wait for installation to complete** (should take 3-5 minutes)

---

## Step 2: Clone the GitHub Repository (2 minutes)

```bash
# Go to home directory
cd ~

# Clone the Dingo OS repository
git clone https://github.com/Baymax005/Dingo-os-.git Dingo-OS

# Navigate to project
cd Dingo-OS

# Verify files exist
ls -la
```

You should see:
- `README.md`
- `PROPOSAL.md`
- `ARCHITECTURE.md`
- `src/` directory
- `Makefile`

---

## Step 3: Build Task Manager (3-5 minutes)

```bash
# Navigate to task-manager directory
cd src/task-manager

# Clean any old builds
make clean

# Build the executable
make
```

**Expected output:**
```
g++ -std=c++11 -Wall -Wextra -O2 -c src/main.cpp -o obj/main.o
g++ -std=c++11 -Wall -Wextra -O2 -c src/process.cpp -o obj/process.o
g++ -std=c++11 -Wall -Wextra -O2 -o ../../../build/bin/task-manager obj/main.o obj/process.o
✓ Built: ../../../build/bin/task-manager
```

✅ If you see "✓ Built", compilation succeeded!

---

## Step 4: Make showip Executable (1 minute)

```bash
# Go back to project root
cd ~/Dingo-OS

# Make showip executable
chmod +x src/showip/showip.sh
```

---

## Step 5: Test Both Utilities (5 minutes)

### Test Task Manager:

```bash
# Show all processes
./build/bin/task-manager

# Should display a table like:
# PID      NAME                 STATE   MEMORY   THREADS
# -------------------------------------------------------
# 1        systemd              S       123 MB   1
# ...
```

Try more commands:
```bash
# Show help
./build/bin/task-manager --help

# Filter processes by name (e.g., bash)
./build/bin/task-manager --filter bash

# Kill a process (it will ask for confirmation)
# Example: find a sleep process and kill it
./build/bin/task-manager --kill 1234  # replace 1234 with a real PID
```

### Test showip:

```bash
# Show all network interfaces
./src/showip/showip.sh

# Should display network interface info

# Test specific interface
./src/showip/showip.sh lo

# Show help
./src/showip/showip.sh --help
```

---

## Step 6: Install to System PATH (Optional but Recommended)

```bash
# Install both utilities to /usr/local/bin
sudo cp build/bin/task-manager /usr/local/bin/
sudo cp src/showip/showip.sh /usr/local/bin/showip
sudo chmod +x /usr/local/bin/showip

# Now you can run from anywhere:
task-manager
showip
```

---

## Step 7: Create Initial Git Commit (if you make changes)

If you modify anything on Ubuntu:

```bash
cd ~/Dingo-OS

# Check what changed
git status

# Add changes
git add -A

# Commit
git commit -m "Testing on Ubuntu VM - all utilities working"

# Push to GitHub
git push origin main
```

---

## Troubleshooting

### Compilation Fails?
```bash
cd src/task-manager
make clean
g++ --version  # Make sure g++ is installed
make
```

### Permission Denied?
```bash
chmod +x src/showip/showip.sh
chmod +x scripts/setup.sh
```

### Task Manager shows no processes?
```bash
# Some processes require root to see
sudo ./build/bin/task-manager

# Or see help
./build/bin/task-manager --help
```

### showip shows no interfaces?
```bash
# Make sure the script is executable
chmod +x src/showip/showip.sh

# Run it
bash src/showip/showip.sh
```

---

## Next Phase: ISO Integration (After Testing)

Once both utilities work on Ubuntu, we'll:

1. **Install Cubic** (ISO remastering tool)
2. **Create Dingo OS ISO** with Task Manager + showip included
3. **Boot ISO in VM** to verify
4. **Test the final product**
5. **Submit for grading**

---

## Quick Reference Commands

```bash
# Build everything
cd ~/Dingo-OS/src/task-manager && make

# Test Task Manager
~/Dingo-OS/build/bin/task-manager

# Test showip
~/Dingo-OS/src/showip/showip.sh

# Install to system
sudo cp ~/Dingo-OS/build/bin/task-manager /usr/local/bin/
sudo cp ~/Dingo-OS/src/showip/showip.sh /usr/local/bin/showip

# Check git status
cd ~/Dingo-OS && git status

# View logs
cd ~/Dingo-OS && git log --oneline
```

---

## When You're Done Testing

Come back here and tell me:
- ✅ Task Manager compiled successfully?
- ✅ Task Manager runs and shows processes?
- ✅ Task Manager can filter by name?
- ✅ Task Manager can kill processes?
- ✅ showip displays network interfaces?

Once all tests pass, we'll move to **ISO Integration**!
