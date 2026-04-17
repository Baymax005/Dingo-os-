# Dingo OS - Cubic Setup Guide (Create Bootable ISO)

**Status**: Ready to create custom ISO  
**Tools needed**: Cubic, VirtualBox/KVM for testing

---

## What is Cubic?

**Cubic** = Custom Ubuntu builder that lets you:
- Start with Ubuntu 22.04 LTS
- Add custom files (your utilities)
- Install extra packages
- Run setup scripts
- Generate bootable ISO

It has a GUI interface that makes ISO creation straightforward.

---

## Step 1: Install Cubic

### On Ubuntu/Debian:

```bash
# Add Cubic PPA
sudo add-apt-repository ppa:cubic-devteam/cubic
sudo apt update

# Install Cubic
sudo apt install cubic
```

### Alternative: Download from Launchpad

Visit: https://launchpad.net/cubic

---

## Step 2: Prepare Your Dingo OS Components

Your project already has everything prepared:

```bash
cd ~/Dingo-OS

# Ensure Task Manager is built
cd src/task-manager && make && cd ../..

# Ensure showip is executable
chmod +x src/showip/showip.sh

# Check build directory
ls -la build/bin/task-manager
ls -la src/showip/showip.sh
```

---

## Step 3: Launch Cubic and Create ISO

### Open Cubic GUI:

```bash
sudo cubic
```

This opens the Cubic graphical interface.

### In Cubic Interface:

#### 1. **Select Base Image**
- Click "Create New Project"
- Select `Ubuntu 22.04 LTS` (or your preferred version)
- Choose destination folder: `~/Dingo-OS/build/iso/`
- Click "Create"

Cubic will extract Ubuntu and prepare the workspace.

#### 2. **Access Custom Disk Terminal**
- In Cubic, click "Terminal" button
- This opens a terminal inside the custom Ubuntu environment
- You're now in `/root/Custom-Disk/` (the new filesystem)

#### 3. **Copy Your Utilities**

In the Cubic terminal:

```bash
# Copy Task Manager
sudo cp /host-path/to/build/bin/task-manager /root/Custom-Disk/usr/local/bin/
sudo chmod +x /root/Custom-Disk/usr/local/bin/task-manager

# Copy showip
sudo cp /host-path/to/src/showip/showip.sh /root/Custom-Disk/usr/local/bin/showip
sudo chmod +x /root/Custom-Disk/usr/local/bin/showip

# Verify
ls -la /root/Custom-Disk/usr/local/bin/ | grep -E "(task-manager|showip)"
```

**Note**: Cubic mounts your real filesystem as `/host/` or similar. Check the path in Cubic's UI.

#### 4. **Install Additional Packages**

In Cubic's "Packages" tab:
- Add packages from `cubic-config/custom-packages.list`
- Example packages to include:
  - `build-essential`
  - `g++` `make` `git`
  - `python3` `python3-pip`
  - `curl` `wget`
  - `vim` `htop`

Or manually in terminal:

```bash
# Inside Cubic's terminal (mounted filesystem)
sudo apt update
sudo apt install -y build-essential g++ make git python3 python3-pip curl wget htop
```

#### 5. **Run Post-Installation Scripts**

In Cubic terminal:

```bash
# Copy and run the setup script
sudo cp /host-path/to/cubic-config/custom-tasks.sh /root/Custom-Disk/opt/
sudo bash /root/Custom-Disk/opt/custom-tasks.sh
```

This will:
- Create necessary directories
- Set file permissions
- Install a welcome message
- Configure the environment

#### 6. **Generate ISO**

Back in Cubic main window:
- Click "Finish" or "Generate ISO"
- Choose filename: `dingo-os.iso`
- Select output location: `~/Dingo-OS/build/iso/`
- Click "Build"

Cubic will compress and create the bootable ISO (takes 5-15 minutes).

---

## Step 4: Verify ISO Was Created

```bash
ls -lh ~/Dingo-OS/build/iso/dingo-os.iso

# Expected output: 
# -rw-r--r-- 1 user user 2.5G dingo-os.iso
```

---

## Step 5: Test the ISO in a Virtual Machine

### Using VirtualBox:

```bash
# Create new VM
# - Name: Dingo OS
# - Type: Linux
# - Version: Ubuntu 64-bit
# - RAM: 2GB minimum
# - Disk: 20GB dynamic

# Attach ISO to CD/DVD drive:
# - Settings → Storage → CD/DVD Drive
# - Choose: ~/Dingo-OS/build/iso/dingo-os.iso
# - Boot from CD/DVD
```

### First Boot:

1. ISO boots Ubuntu installer
2. Choose your preferred installation options
3. After installation completes, reboot
4. Log in with credentials (configured in preseed.cfg)

### Verify Utilities Are Installed:

```bash
# After logging in to Dingo OS
task-manager --help
showip --help

# Or run them
task-manager
showip
```

---

## Step 6: Troubleshooting

### "Cubic not found"
```bash
# Install Cubic first
sudo apt install cubic
```

### "Utils not showing up in ISO"
- Double-check `/usr/local/bin/` path in Cubic
- Ensure you used `sudo cp` to copy files
- Verify file permissions: `chmod +x`

### "ISO too large"
- Remove unnecessary packages from preseed
- Don't include heavy desktop environments

### "ISO won't boot"
- Try UEFI mode in VM settings
- Check ISO integrity: `sha256sum dingo-os.iso`
- Recreate if corrupted

---

## Complete Workflow Summary

```
┌────────────────────────────────────┐
│ 1. Build Task Manager              │
│    cd src/task-manager && make     │
└────────────────┬───────────────────┘
                 │
┌────────────────▼───────────────────┐
│ 2. Launch Cubic                    │
│    sudo cubic                      │
└────────────────┬───────────────────┘
                 │
┌────────────────▼───────────────────┐
│ 3. Create Project (Ubuntu 22.04)   │
│    Select base image & workspace   │
└────────────────┬───────────────────┘
                 │
┌────────────────▼───────────────────┐
│ 4. Copy Utilities to /usr/local/bin│
│    task-manager, showip            │
└────────────────┬───────────────────┘
                 │
┌────────────────▼───────────────────┐
│ 5. Install Packages                │
│    build-essential, python3, etc   │
└────────────────┬───────────────────┘
                 │
┌────────────────▼───────────────────┐
│ 6. Run Setup Scripts               │
│    custom-tasks.sh                 │
└────────────────┬───────────────────┘
                 │
┌────────────────▼───────────────────┐
│ 7. Generate ISO                    │
│    → dingo-os.iso                  │
└────────────────┬───────────────────┘
                 │
┌────────────────▼───────────────────┐
│ 8. Test Boot in VM                 │
│    Verify utilities work           │
└────────────────────────────────────┘
```

---

## What's in Your ISO?

When complete, your `dingo-os.iso` will include:

✅ Ubuntu 22.04 LTS base  
✅ Task Manager (C++ binary)  
✅ showip (Bash script)  
✅ ding package manager (when ready)  
✅ Build tools (g++, make, python3)  
✅ System utilities (git, curl, htop, vim)  
✅ Custom welcome message  
✅ Pre-configured boot settings  

---

## Next Steps After ISO Creation

1. ✅ Create ISO with Cubic
2. ✅ Boot and test in VM
3. ✅ Verify all utilities work
4. ✅ Document any issues
5. ✅ Prepare submission package

Once ISO boots successfully and all utilities function, your Dingo OS distribution is complete!

---

## Need Help?

- Cubic documentation: https://github.com/PJ-Singh-001/Cubic/wiki
- Ubuntu preseed reference: https://help.ubuntu.com/lts/installation-guide/
- Report issues: GitHub issues or project documentation

---

**You're ready to build your first custom Linux distribution! 🎉**
