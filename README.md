# 🐧 Dingo OS - Custom Linux Distribution

A custom Ubuntu-based Linux distribution with enhanced CLI utilities for package management, network administration, and system security.

---

## 📊 Project Status

### v1 - ✅ COMPLETE
- **Status**: Bootable ISO ready for deployment
- **Deliverables**: Task Manager, showip, ding, and bootable ISO
- **Build Time**: ~1 week
- **Testing**: Tested on VirtualBox and bare metal

### v2 - 🚀 IN DEVELOPMENT (1.5 weeks)
- **Focus**: Package manager enhancements + security auditing
- **Components**: ding v2, dingo-audit
- **Target**: Complete by end of sprint

---

## 🎯 Core Components

### v1 Features (READY ✅)

**v1 has 2 core components**

#### 1. **Task Manager** (C++ Process Monitor)
Monitor and control system processes with a clean CLI interface.

```bash
task-manager              # List all processes
task-manager --filter bash        # Filter by name
task-manager --kill <PID>         # Terminate process (with confirmation)
task-manager --help              # Show help
```

**What it does**:
- Reads `/proc` filesystem for process information
- Display: PID, process name, state, memory, threads
- Kill processes with user confirmation
- Filter by process name

**Files**: `src/task-manager/`

---

#### 2. **showip** (Network Utilities)
Quick and simple network interface information display.

```bash
showip                   # Show all interfaces
showip eth0              # Show specific interface
showip --help            # Show help
```

**What it does**:
- Display active network interfaces
- Show IP addresses (IPv4/IPv6)
- Parse network device statistics
- Clean, readable output

**Files**: `src/showip/`

---

### v2 Features (BUILDING 🚀)

#### 1. **ding v2** (Enhanced Package Manager)
Smart package manager with caching, repos, and plugins.

**New Features**:
- ✨ **Smart Caching**: Cache searches for speed
- 📦 **Repository Management**: Add/remove PPAs
- 🔌 **Plugin System**: Extend with custom commands
- ⚡ **Performance**: <100ms for cached results vs 2-3s uncached

```bash
# Caching
ding cache-stats         # Show cache usage
ding cache-clean         # Clear cache

# Repository management
ding repo add ubuntu-security ppa:ubuntu/security
ding repo list
ding repo remove ubuntu-security

# Plugins
ding plugin list
ding plugin load my-commands.py
```

**Files**: `v2/src/ding-v2/`

---

#### 2. **dingo-audit** (Security Scanner)
Quick vulnerability and system forensics scanner.

**Scan Modes**:
- 🟢 **Quick** (<30s): Fast port and permission checks
- 🟡 **System** (~5m): Deep system security audit
- 🔵 **Network**: Local network enumeration
- 🔴 **All** (~10m): Complete system + network scan

```bash
# Quick scan
dingo-audit --quick

# Full system audit
dingo-audit --system

# Network scan
dingo-audit --network

# Complete audit with export
dingo-audit --all --verbose --output audit-report.txt
```

**What it checks**:
- Open ports and listening services
- Running services and daemons
- Critical file permissions (/etc/passwd, /etc/shadow, /etc/sudoers)
- User accounts and sudoers configuration
- Firewall status
- Available security updates
- Recent system logs
- Network interfaces and active connections
- Local network devices

**Files**: `v2/src/dingo-audit/`

---

## 📁 Project Structure

```
Dingo-OS/
│
├── v1/ (STABLE - 2 Components)
│   ├── src/
│   │   ├── task-manager/     ✅ Complete (C++)
│   │   └── showip/           ✅ Complete (Bash)
│   │
│   ├── build/
│   │   ├── bin/              # Compiled binaries
│   │   └── iso/              # Generated ISO
│   │
│   ├── UBUNTU_SETUP_GUIDE.md
│   └── CUBIC_SETUP_GUIDE.md
│
├── v2/ (IN DEVELOPMENT - 2 Components)
│   ├── src/
│   │   ├── ding-v2/          🚀 In progress (Python)
│   │   │   ├── ding.py
│   │   │   ├── cache_manager.py
│   │   │   ├── repo_manager.py
│   │   │   └── plugin_loader.py
│   │   │
│   │   └── dingo-audit/      ✅ Ready (Bash)
│   │       ├── dingo-audit.sh
│   │       └── README.md
│   │
│   ├── docs/
│   │   ├── V2_ROADMAP.md
│   │   └── DING_v2_GUIDE.md
│   │
│   └── V2_ROADMAP.md         # Development plan
│
├── docs/
│   ├── ARCHITECTURE.md       # System design
│   └── PROPOSAL.md           # Project proposal
│
├── README.md                 # This file
└── .gitignore
```

---

## 🚀 Quick Start

### Build v1 (Complete)

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential g++ git make python3

# 2. Clone repository
cd ~
git clone https://github.com/Baymax005/Dingo-os-.git Dingo-OS
cd Dingo-OS

# 3. Build Task Manager
cd src/task-manager && make && cd ../..

# 4. Make showip executable
chmod +x src/showip/showip.sh

# 5. Test utilities
./build/bin/task-manager --help
./src/showip/showip.sh --help

# 6. Install to system (optional)
sudo cp build/bin/task-manager /usr/local/bin/
sudo cp src/showip/showip.sh /usr/local/bin/showip
```

### Create v1 ISO with Cubic

```bash
# 1. Install Cubic
sudo apt install cubic

# 2. Open Cubic GUI
sudo cubic

# 3. Follow CUBIC_SETUP_GUIDE.md
# - Select Ubuntu 22.04 LTS
# - Copy utilities to /usr/local/bin/
# - Add packages
# - Generate ISO

# 4. Boot ISO in VirtualBox
```

### Build v2 (In Progress)

```bash
# 1. ding v2 development
cd v2/src/ding-v2
# [Working on cache_manager, repo_manager, plugin_loader]

# 2. dingo-audit ready
chmod +x v2/src/dingo-audit/dingo-audit.sh
v2/src/dingo-audit/dingo-audit.sh --quick
```

---

## 📖 Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture (v1 + v2)
- **[PROPOSAL.md](PROPOSAL.md)** - Project proposal and goals
- **[UBUNTU_SETUP_GUIDE.md](UBUNTU_SETUP_GUIDE.md)** - v1 setup on Ubuntu
- **[CUBIC_SETUP_GUIDE.md](CUBIC_SETUP_GUIDE.md)** - v1 ISO creation guide
- **[v2/V2_ROADMAP.md](v2/V2_ROADMAP.md)** - v2 development plan
- **[v2/docs/DING_v2_GUIDE.md](v2/docs/DING_v2_GUIDE.md)** - ding v2 features
- **[v2/src/dingo-audit/README.md](v2/src/dingo-audit/README.md)** - dingo-audit usage

---

## 🔧 Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Task Manager | C++ | Process monitoring, performance |
| showip | Bash | Network utilities, simplicity |
| ding v1 | Python/Bash | Package management wrapper |
| ding v2 | Python | Enhanced package manager |
| dingo-audit | Bash | Security scanning |
| ISO Generation | Cubic + Bash | Custom Ubuntu remastering |
| Base OS | Ubuntu 22.04 LTS | Stable Debian ecosystem |

---

## 📋 Development Timeline

### v1 Timeline (COMPLETED ✅)
- Week 1: Design + build all components
- Week 2: ISO creation and testing
- **Status**: Ready for deployment

### v2 Timeline (IN PROGRESS 🚀)
- **Days 1-5**: ding v2 core development (caching, repos, plugins)
- **Days 6-8**: Integration and testing
- **Days 9-11**: Documentation and polish
- **Days 12-13**: Final submission
- **Target**: 1.5 weeks from now

---

## 🎓 Learning Outcomes

### Concepts Demonstrated

1. **Linux Process Management**
   - Reading `/proc/[pid]/` filesystem
   - Process state parsing
   - Memory and CPU calculation
   - Signal handling (SIGKILL)

2. **System Programming**
   - C++ file I/O and string parsing
   - Bash scripting and command execution
   - Python subprocess and OS modules
   - System call integration

3. **Package Management**
   - apt/apt-cache ecosystem
   - Repository management
   - Dependency resolution basics
   - CLI wrapper design

4. **Security & Auditing**
   - Vulnerability scanning principles
   - System security posture assessment
   - Network enumeration
   - Forensic data collection

5. **Linux Distribution**
   - ISO generation and remastering
   - Bootable system creation
   - Preseed configuration
   - Custom system initialization

---

## 🧪 Testing

### v1 Verification Checklist
- [x] Task Manager compiles without errors
- [x] Task Manager displays processes
- [x] Task Manager can filter by name
- [x] Task Manager can kill processes
- [x] showip displays network interfaces
- [x] ding wraps apt commands correctly
- [x] ISO boots successfully
- [x] All utilities available in PATH
- [x] Welcome message displays on boot

### v2 Testing (In Progress)
- [ ] ding v2 cache operations work
- [ ] Repository management functional
- [ ] Plugin loading and execution
- [ ] dingo-audit all scan modes work
- [ ] Export to file functionality
- [ ] Integration between components

---

## 🐛 Troubleshooting

### Task Manager Issues
```bash
# Compilation fails
cd src/task-manager && make clean && make

# No processes shown
sudo ./build/bin/task-manager  # Need root for all processes

# Permission denied
chmod +x src/showip/showip.sh
chmod +x scripts/*.sh
```

### ISO Creation Issues
```bash
# Cubic not installed
sudo apt install cubic

# ISO won't boot
# - Try UEFI mode in VM settings
# - Check ISO integrity: sha256sum dingo-os.iso
# - Recreate if corrupted
```

### ding Issues
```bash
# apt not found
sudo apt update  # Install apt first

# Permission denied
sudo ding install package-name  # Some operations need sudo
```

---

## 📝 Contributing

To contribute to Dingo OS:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Muhammad Ali**

- GitHub: [@Baymax005](https://github.com/Baymax005)
- Project: [Dingo-os-](https://github.com/Baymax005/Dingo-os-)

---

## 🎉 Acknowledgments

- Ubuntu community for base OS
- Cubic project for ISO remastering
- Contributors and testers

---

## 📞 Support

For issues, questions, or suggestions:
- Check existing GitHub issues
- Create a new GitHub issue with details
- Review documentation in `docs/` folder

---

**Dingo OS - Making Linux simpler, one utility at a time! 🐕**
