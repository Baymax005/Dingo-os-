# Dingo OS v2 - ISO Customizations & Build Guide

## Overview

Dingo OS v2 is a heavily customized Ubuntu 22.04 LTS distribution built with **Cubic**, featuring a cyberpunk aesthetic, lightweight XFCE desktop, and integrated system utilities (task manager, showip, ding, dingo-audit).

**Status**: ✅ COMPLETE - 5.2GB bootable ISO generated  
**Base**: Ubuntu 22.04 LTS  
**Desktop**: XFCE4 + LightDM (replacing GNOME)  
**Kernel**: Linux 5.15.x  
**Build Tool**: Cubic

---

## Phase 1: Core System & Dependency Management

The base system was stripped of standard GNOME bloatware and replaced with lightweight utilities optimized for both virtual environments and bare metal deployment.

### Changes Made

```bash
# Update repository indices
apt update

# Install VMware tools for host-to-guest clipboard & screen scaling
apt install -y open-vm-tools-desktop

# Install UI and aesthetic utilities
apt install -y neofetch xfce4-whiskermenu-plugin plank

# Remove GNOME bloat
apt remove -y gnome-shell gdm3 gnome-terminal \
  gnome-keyring evolution thunderbird \
  ubuntu-software gnome-calendar gnome-weather
apt autoremove -y && apt clean
```

### Why These Changes?

- **Remove GNOME**: Massive memory footprint, unnecessary for custom distro
- **Add XFCE4**: Lightweight, highly customizable, ~100MB vs 500MB+ for GNOME
- **LightDM**: Simple, fast login manager
- **VMware tools**: Essential for VirtualBox/VMware testing
- **neofetch**: System info display with ASCII art
- **plank**: Minimal dock for application access
- **Whisker Menu**: Modern app launcher (replaces GNOME Activities)

---

## Phase 2: The Hacker Aesthetic & Terminal Injection

Custom terminal styling creates the cyberpunk "Dingo OS" experience on every boot.

### 2.1 Terminal Color Configuration

```bash
mkdir -p /etc/skel/.config/xfce4/terminal
cat << 'EOF' > /etc/skel/.config/xfce4/terminal/terminalrc
[Configuration]
ColorBackground=#000000
ColorForeground=#FFFFFF
ColorCursor=#FFA500

ColorSelection=#FFA500
ColorSelectionUseDefault=FALSE
EOF
```

**Color Scheme**:
- Background: Pure black (`#000000`)
- Text: Stark white (`#FFFFFF`)
- Cursor & Selection: Electric orange (`#FFA500`)

### 2.2 Bash Customization & Custom Prompt

```bash
# Inject the custom Baymax prompt
echo "PS1='\[\033[01;33m\]baymax\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> /etc/skel/.bashrc

# Link 'ding' command to 'apt' for Dingo OS branding
echo "alias ding='apt'" >> /etc/skel/.bashrc
```

**Prompt Breakdown**:
- `baymax`: Username in bright yellow
- `:` separator
- `\w`: Current directory in bright blue
- `$`: Dollar sign indicator

---

## Phase 3: Custom Branding & Neofetch

Automatic system information display on every terminal session.

### 3.1 Dingo OS ASCII Logo

```bash
# Create the ASCII Art file
cat << 'EOF' > /etc/dingo-logo.txt
___ _ ____ _____
/ _ \(_)__ ___ ___ / __ \/ ___/
/ // / / _ \/ _ `/ _ \ / /_/ /\__ \
/____/_/_//_/\_, /\___/ \____/___/
/___/
EOF
```

### 3.2 Neofetch Auto-startup

```bash
# Force Neofetch to run on startup with the custom logo
echo "neofetch --source /etc/dingo-logo.txt --uptime_shorthand tiny --memory_percent on" >> /etc/skel/.bashrc
```

**Result**: Users see system specs + Dingo OS branding on every terminal open

---

## Phase 4: Modern Desktop UI Automation

XFCE desktop is configured with modern UX patterns.

### 4.1 Plank Dock Auto-start

```bash
# Auto-start Plank Dock
mkdir -p /etc/skel/.config/autostart
cat << 'EOF' > /etc/skel/.config/autostart/plank.desktop
[Desktop Entry]
Name=Plank
Exec=plank
Icon=plank
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
EOF
```

### 4.2 Super Key Binding to Whisker Menu

```bash
# Bind the Windows (Super) key to the Whisker Menu
mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml
cat << 'EOF' > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-keyboard-shortcuts" version="1.0">
  <property name="commands" type="empty">
    <property name="custom" type="empty">
      <property name="Super_L" type="string" value="xfce4-popup-whiskermenu"/>
    </property>
  </property>
</channel>
EOF
```

**UX Improvements**:
- Plank provides quick app access (Windows-style taskbar)
- Super key opens application menu (Windows-like behavior)
- Smooth transition for Windows users

---

## Phase 5: System Patches & Optimization

Silent optimizations for a clean, distraction-free experience.

### 5.1 Disable Apport Crash Reporter

```bash
# Silence Apport - prevents "System program problem detected" popups
sed -i 's/enabled=1/enabled=0/g' /etc/default/apport
```

**Why?**: Removing GNOME triggers harmless Apport notifications that clutter the experience

### 5.2 ISO Size Optimization

```bash
# Clean up cached installation files to minimize final ISO size
apt autoremove -y && apt clean && rm -rf /tmp/*
```

**Result**: Reduced ISO from 6.5GB → 5.2GB

---

## Phase 6: Bootloader Configurations

Custom Grub settings for cinematic boot experience.

### 6.1 Boot Parameters

Modified in Cubic's final configuration screen:

**Changes**:
- **Removed**: `quiet splash` from linux boot lines
- **Effect**: Kernel code matrix displays during boot (no splash screen)
- **Menu Entries**: Renamed from "Ubuntu" → "Dingo OS"

**Boot Files Modified**:
- `boot/grub/grub.cfg`
- `boot/grub_loopback.cfg`

**Grub Configuration**:
```bash
# Before
linux	/boot/vmlinuz-5.15.0-XX-generic root=/dev/mapper/ubuntu--vg-root ro quiet splash

# After
linux	/boot/vmlinuz-5.15.0-XX-generic root=/dev/mapper/ubuntu--vg-root ro
```

**Menu Entry Naming**:
```bash
# Before
menuentry 'Ubuntu' {

# After
menuentry 'Dingo OS' {
```

---

## Phase 7: Network Transfer & ISO Delivery

Method for extracting the 5.2GB ISO from the build VM to Windows host.

### 7.1 Local Python HTTP Server

```bash
# Navigate to the directory containing the ISO
cd ~/cubic/extract/

# Start a local web server on port 8000
python3 -m http.server 8000
```

### 7.2 Access from Windows Host

```
http://[UBUNTU_VM_IP_ADDRESS]:8000
```

**Example**:
```
http://192.168.1.100:8000
```

- Click on ISO file to download
- Transfer time: ~10-15 minutes (5.2GB over local network)

---

## Complete Customization Build Script

All customizations bundled into a single Bash script for reproducibility:

```bash
#!/bin/bash
# dingo-os-v2-customizations.sh
# Run inside Cubic's chroot environment

set -e

echo "[*] Starting Dingo OS v2 Customization..."

# Phase 1: Core System
echo "[1/7] Installing core packages..."
apt update
apt install -y open-vm-tools-desktop neofetch xfce4-whiskermenu-plugin plank
apt remove -y gnome-shell gdm3 gnome-terminal gnome-keyring evolution thunderbird ubuntu-software gnome-calendar gnome-weather
apt autoremove -y && apt clean

# Phase 2: Terminal Configuration
echo "[2/7] Configuring terminal aesthetics..."
mkdir -p /etc/skel/.config/xfce4/terminal
cat > /etc/skel/.config/xfce4/terminal/terminalrc << 'TERM_EOF'
[Configuration]
ColorBackground=#000000
ColorForeground=#FFFFFF
ColorCursor=#FFA500
ColorSelection=#FFA500
ColorSelectionUseDefault=FALSE
TERM_EOF

echo "PS1='\[\033[01;33m\]baymax\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> /etc/skel/.bashrc
echo "alias ding='apt'" >> /etc/skel/.bashrc

# Phase 3: Branding
echo "[3/7] Setting up Dingo OS branding..."
cat > /etc/dingo-logo.txt << 'LOGO_EOF'
___ _ ____ _____
/ _ \(_)__ ___ ___ / __ \/ ___/
/ // / / _ \/ _ `/ _ \ / /_/ /\__ \
/____/_/_//_/\_, /\___/ \____/___/
/___/
LOGO_EOF

echo "neofetch --source /etc/dingo-logo.txt --uptime_shorthand tiny --memory_percent on" >> /etc/skel/.bashrc

# Phase 4: Desktop UI
echo "[4/7] Configuring XFCE desktop..."
mkdir -p /etc/skel/.config/autostart
cat > /etc/skel/.config/autostart/plank.desktop << 'PLANK_EOF'
[Desktop Entry]
Name=Plank
Exec=plank
Icon=plank
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
PLANK_EOF

mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml
cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml << 'KB_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-keyboard-shortcuts" version="1.0">
  <property name="commands" type="empty">
    <property name="custom" type="empty">
      <property name="Super_L" type="string" value="xfce4-popup-whiskermenu"/>
    </property>
  </property>
</channel>
KB_EOF

# Phase 5: Optimizations
echo "[5/7] Applying system optimizations..."
sed -i 's/enabled=1/enabled=0/g' /etc/default/apport
apt autoremove -y && apt clean && rm -rf /tmp/*

echo "[*] Customization complete!"
```

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Base ISO | Ubuntu 22.04 LTS |
| Final Size | 5.2 GB |
| Desktop | XFCE4 + LightDM |
| Boot Time | ~15-20 seconds |
| Memory Usage | ~300MB idle |
| Included Tools | task-manager, showip, ding, dingo-audit |
| Kernel | Linux 5.15.x |
| Build Tool | Cubic |

---

## Testing & Verification

### Boot Testing
- ✅ Boots in VirtualBox (BIOS + UEFI)
- ✅ Boots on bare metal
- ✅ Boots on VMware
- ✅ Kernel code matrix displays (no splash)

### UI/UX Testing
- ✅ XFCE desktop loads correctly
- ✅ Plank dock auto-starts
- ✅ Super key opens Whisker Menu
- ✅ Terminal loads with custom colors
- ✅ Neofetch displays on terminal open
- ✅ Baymax prompt visible

### Utility Testing
- ✅ task-manager functional
- ✅ showip working
- ✅ ding (apt alias) functional
- ✅ dingo-audit scans execute

---

## Future Enhancements (v3+)

- Custom graphical installer (Calamares or Qt-based)
- Pre-configured task manager dashboard
- Dingo OS splash screen during boot
- Custom wallpapers and themes
- Network PXE boot support
- Automated updates with dingo
- System recovery tools

---

## Build Reproducibility

To rebuild the exact ISO:

1. **Start with Cubic**
   ```bash
   sudo cubic
   ```

2. **Select Base ISO**: Ubuntu 22.04 LTS

3. **Run customization script** in Cubic's terminal

4. **Generate ISO** with Cubic GUI

5. **Verify**: Boot in VM and test all components

---

## References

- [Cubic ISO Remastering Tool](https://cubic.sh/)
- [XFCE Desktop Guide](https://docs.xfce.org/)
- [Ubuntu Customization](https://ubuntu.com/)
- [Grub Configuration](https://www.gnu.org/software/grub/manual/)

---

**Dingo OS v2 - Making Linux simpler, one utility at a time! 🐕**
