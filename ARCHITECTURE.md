# Dingo OS - Architecture & Structure

## 1. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        DINGO OS (Custom ISO)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────── User Layer ──────────────────────┐    │
│  │  Custom CLI Tools (Integrated in $PATH)               │    │
│  │  ┌─────────────────┐  ┌──────────────────┐           │    │
│  │  │   ding          │  │   showip         │           │    │
│  │  │ (pkg manager)   │  │ (network utils)  │           │    │
│  │  └────────┬────────┘  └────────┬─────────┘           │    │
│  │           │                    │                      │    │
│  └───────────┼────────────────────┼──────────────────────┘    │
│              │                    │                           │
│  ┌───────────┼────────────────────┼──────────────────────┐    │
│  │ Task Manager Layer               │                   │    │
│  │  ┌────────────────────────────────────┐              │    │
│  │  │  Custom Task Manager (C++/Python)  │              │    │
│  │  │  - Process monitoring              │              │    │
│  │  │  - Resource tracking               │              │    │
│  │  │  - Process control (kill/pause)    │              │    │
│  │  └────────────────┬───────────────────┘              │    │
│  └───────────────────┼──────────────────────────────────┘    │
│                      │                                        │
│  ┌───────────────────┼──────────────────────────────────┐    │
│  │ System Interface Layer                               │    │
│  │  ┌──────────────────────────────────────────────┐   │    │
│  │  │ Linux Kernel & System Call Interface         │   │    │
│  │  │ - /proc filesystem parsing                   │   │    │
│  │  │ - apt package system (via wrapper)           │   │    │
│  │  │ - ip command interface                       │   │    │
│  │  │ - Process control syscalls (kill, etc)       │   │    │
│  │  └──────────────────────────────────────────────┘   │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌──────────────────── Ubuntu Base (LTS) ────────────────┐    │
│  │ Kernel | Package System (apt) | Core Utilities        │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Dingo OS v2 - Enhanced Architecture

**Status**: v2 Development (1.5 weeks)

Dingo OS v2 builds on v1 with enhanced tooling for package management and security auditing.

### v2 Component Overview

```
┌──────────────────────────────────────────────────────┐
│          Dingo OS v2 (Enhanced)                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────── User Layer ──────────────┐           │
│  │  Advanced CLI Tools (in $PATH)       │           │
│  │  ┌──────────┐  ┌──────────────┐    │           │
│  │  │ ding v2  │  │ dingo-audit  │    │           │
│  │  │(enhanced)│  │(security)    │    │           │
│  │  └──────────┘  └──────────────┘    │           │
│  │                                      │           │
│  │  ★ Smart caching                    │           │
│  │  ★ Repository management           │           │
│  │  ★ Basic plugin system             │           │
│  │  ★ Vulnerability scanning          │           │
│  │  ★ System forensics                │           │
│  └──────────────────────────────────────┘           │
│                                                      │
│  ┌──── v1 Components (Unchanged) ────┐             │
│  │  • task-manager (process monitor)  │             │
│  │  • showip (network utilities)      │             │
│  │  • ding v1 (basic apt wrapper)     │             │
│  └────────────────────────────────────┘             │
│                                                      │
│  ┌─────── Ubuntu 22.04 LTS Base ───────┐           │
│  │ Kernel | apt | Core System          │           │
│  └──────────────────────────────────────┘           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### v2 New Components

#### 2.1 ding v2 - Enhanced Package Manager

**Purpose**: Extend ding v1 with intelligent caching, repository management, and plugin support

**Architecture**:
```
ding v2 (Main CLI)
├── cache_manager.py
│   ├── Cache storage (~/.dingo/cache/)
│   ├── TTL management
│   ├── Index rebuilding
│   └── Size limiting
│
├── repo_manager.py
│   ├── Repository list management
│   ├── Add/remove PPA handling
│   ├── Enable/disable repos
│   └── Sources.list integration
│
├── plugin_loader.py
│   ├── Plugin discovery
│   ├── Dynamic loading
│   ├── Hook execution
│   └── Plugin directory (~/.dingo/plugins/)
│
└── ding.py (v1 wrapper with v2 features)
    ├── Backward compatible
    ├── Cache integration
    ├── Plugin orchestration
    └── apt execution
```

**Key Features**:
- **Smart Caching**: Store search results with TTL (24h default)
- **Repository Management**: Add/remove/enable/disable PPAs
- **Plugin System**: Load custom commands via Python plugins
- **Performance**: <100ms cached searches vs 2-3s uncached

**Files**:
- `v2/src/ding-v2/ding.py` - Main entry point
- `v2/src/ding-v2/cache_manager.py` - Caching system
- `v2/src/ding-v2/repo_manager.py` - Repository management
- `v2/src/ding-v2/plugin_loader.py` - Plugin system

**Interfaces**:
```bash
ding cache-stats              # Show cache usage
ding cache-clean              # Clear cache
ding repo add NAME PPA         # Add repository
ding repo list                 # List all repos
ding repo remove NAME          # Remove repository
ding plugin list               # Show plugins
ding plugin load FILE          # Load plugin
```

**Dependencies**: `apt`, `apt-cache`, Python 3.8+

---

#### 2.2 dingo-audit - Security Scanner

**Purpose**: Quick vulnerability and forensic assessment of system and network

**Architecture**:
```
dingo-audit (Bash Script)
├── System Audit Module
│   ├── Open ports check (ss/netstat)
│   ├── Service enumeration (systemctl)
│   ├── File permissions audit
│   ├── User account review
│   ├── Firewall status
│   ├── Security updates check
│   └── System logs analysis
│
├── Network Audit Module
│   ├── Network interface enumeration
│   ├── Active connections listing
│   ├── Local network scanning (nmap)
│   └── Connection detail analysis
│
└── Output System
    ├── Console output (default)
    ├── File export (--output)
    ├── Verbose mode (--verbose)
    └── Color formatting
```

**Key Features**:
- **Quick Scan**: <30 seconds for fast checks
- **System Audit**: <5 minutes for deep scan
- **Network Scan**: Local network enumeration
- **Full Audit**: Combined system + network scan
- **Export**: Save reports to file

**Files**:
- `v2/src/dingo-audit/dingo-audit.sh` - Main scanner
- `v2/src/dingo-audit/README.md` - Usage guide

**Interfaces**:
```bash
dingo-audit --quick           # Fast port/permission check
dingo-audit --system          # Deep system audit
dingo-audit --network         # Network scan
dingo-audit --all             # Full audit
dingo-audit --verbose         # Detailed output
dingo-audit --output FILE     # Export to file
dingo-audit --help            # Show help
```

**Dependencies**: `ss/netstat`, `systemctl`, `ufw/iptables`, optional `nmap`

---

### v2 Data Flow

```
User Input (CLI)
    │
    ├─→ ding v2
    │   ├─ Check cache_manager
    │   ├─ Load plugins
    │   ├─ Manage repos
    │   └─ Execute apt
    │
    └─→ dingo-audit
        ├─ Run system checks
        ├─ Run network scans
        ├─ Format output
        └─ Export report
```

---

### v2 Configuration

**ding v2 Config** (`~/.dingo/ding.conf`):
```yaml
cache:
  enabled: true
  max-size: 500M
  ttl: 86400

repositories:
  - name: ubuntu-main
    enabled: true
  - name: ubuntu-security
    enabled: true

plugins:
  enabled:
    - custom-search
  disabled: []
```

**dingo-audit Config** (command-line only):
- No persistent config
- Modes controlled via flags

---

## 3. Component Specifications

### 2.1 ding - Package Manager Wrapper

**Purpose**: Simplify `apt` package management with an intuitive CLI

**Architecture**:
```
ding (CLI Entry Point)
├── Parser: Commands (install, remove, update, search)
├── Config Manager: ~/.dingo/ding.conf (YAML)
├── apt Executor: Shells out to apt with parsed args
├── Output Formatter: Human-readable results
└── Error Handler: Friendly error messages
```

**Key Files**:
- `ding.py` - Core logic (Python 3.8+)
- `ding.sh` - Shell wrapper for system integration
- `config.yaml` - User preferences & aliases

**Interfaces**:
```bash
ding install <package>        # Install a package
ding remove <package>         # Remove a package
ding update                   # Update package lists
ding upgrade                  # Upgrade installed packages
ding search <term>            # Search for packages
ding info <package>           # Show package details
ding clean                    # Clean cache
```

**Dependencies**: `apt`, `apt-cache`, Python 3.8+

---

### 2.2 showip - Network Utilities Wrapper

**Purpose**: Simplify network interface and connectivity information display

**Architecture**:
```
showip (Shell Script)
├── Parse args (--detailed, --json, filter)
├── Execute ip commands
├── Parse /proc/net/* files for detailed info
├── Format output (tabular, JSON)
└── Display to user
```

**Key Files**:
- `showip.sh` - Main implementation (Bash)

**Interfaces**:
```bash
showip                        # Show all interfaces
showip eth0                   # Show specific interface
showip --detailed             # Verbose output
showip --json                 # JSON output for scripting
showip --dns                  # Show DNS configuration
```

**Data Sources**:
- `ip addr show` - Interface info
- `/proc/net/dev` - Network statistics
- `/etc/resolv.conf` - DNS info
- `ip route show` - Routing info

**Dependencies**: `ip`, `awk`, standard utilities

---

### 2.3 Task Manager - Process Monitor & Controller

**Purpose**: Display and manage system processes with kernel-level insights

**Architecture**:
```
Task Manager (C++ Binary)
├── /proc File Parser
│   ├── Read /proc/[pid]/stat - process state
│   ├── Read /proc/[pid]/status - memory info
│   ├── Read /proc/[pid]/cmdline - command
│   └── Read /proc/stat - system stats
├── Process Data Model
│   ├── Process struct (PID, name, CPU, memory, state)
│   ├── Sort/Filter engine
│   └── Cache (update interval configurable)
├── Display Engine
│   ├── Terminal UI (ncurses or simple table)
│   ├── Real-time updates
│   └── Sortable columns
├── Process Control
│   ├── kill(2) syscall for termination
│   ├── pause/resume via signals
│   └── Confirmation prompts
└── Resource Monitor
    ├── CPU usage (aggregate & per-process)
    ├── Memory (used, available, swap)
    ├── Uptime & load average
    └── System-wide statistics
```

**Key Files**:
- `task-manager.cpp` - Main implementation
- `task-manager.h` - Header/API
- `Makefile` - Build configuration
- `tests/test-task-manager.cpp` - Unit tests

**Interfaces**:
```bash
task-manager                  # Interactive mode (live dashboard)
task-manager --list          # List all processes (non-interactive)
task-manager --filter <name> # Filter by process name
task-manager --sort cpu      # Sort by CPU usage
task-manager --kill <pid>    # Terminate process (with confirmation)
task-manager --help          # Show help
```

**Data Structures**:
```cpp
struct Process {
    int pid;
    string name;
    string state;           // R, S, D, Z, T
    int threads;
    int parent_pid;
    double cpu_percent;
    long memory_kb;
    long rss_kb;
    string cmdline;
    long start_time;
};

struct SystemStats {
    long uptime;
    double load_avg[3];     // 1min, 5min, 15min
    long total_memory;
    long available_memory;
    long cpu_cores;
};
```

**Dependencies**: Standard C++ library, Linux headers

---

## 3. Data Flow Diagram

```
User Input
    │
    ├─→ ding (Command: apt interaction flow)
    │   ├─ Parse args
    │   ├─ Validate command
    │   ├─ Execute apt command
    │   ├─ Parse apt output
    │   └─ Display formatted result ───→ Output
    │
    ├─→ showip (Command: Network info flow)
    │   ├─ Parse args
    │   ├─ Execute ip commands
    │   ├─ Read /proc/net/* files
    │   ├─ Format output
    │   └─ Display ───→ Output
    │
    └─→ task-manager (Interactive flow)
        ├─ Read /proc/[pid]/* files
        ├─ Parse process data
        ├─ Apply filters/sorting
        ├─ Display table/UI
        ├─ Wait for user input
        ├─ If kill/pause: escalate with confirmation
        ├─ Send signal to process
        └─ Update display ───→ Output
```

---

## 4. Directory Structure (Detailed)

```
dingo-os/
│
├── PROPOSAL.md                          # Project proposal
├── ARCHITECTURE.md                      # This file
├── README.md                            # Quick start guide
├── LICENSE                              # Project license
│
├── cubic-config/                        # Cubic remastering config
│   ├── preseed.cfg                      # Ubuntu preseed configuration
│   ├── custom-packages.list             # APT packages to include
│   ├── custom-tasks.sh                  # Post-install scripts
│   └── boot-splash.png                  # Custom splash image
│
├── src/                                 # Source code
│   │
│   ├── ding/                            # Package manager wrapper
│   │   ├── ding.py                      # Main logic (Python)
│   │   ├── ding.sh                      # Shell wrapper
│   │   ├── config.yaml                  # Default configuration
│   │   ├── README.md                    # ding documentation
│   │   └── examples/
│   │       └── ding.conf.example        # Config template
│   │
│   ├── showip/                          # Network utilities wrapper
│   │   ├── showip.sh                    # Main implementation
│   │   ├── README.md                    # showip documentation
│   │   └── examples/
│   │       └── sample-output.txt        # Example output
│   │
│   └── task-manager/                    # Process monitor
│       ├── src/
│       │   ├── main.cpp
│       │   ├── process.cpp
│       │   ├── process.h
│       │   ├── system.cpp
│       │   ├── system.h
│       │   ├── parser.cpp
│       │   └── parser.h
│       ├── Makefile                     # Build configuration
│       ├── Makefile.debug               # Debug build
│       ├── tests/
│       │   ├── test-parser.cpp
│       │   ├── test-system.cpp
│       │   └── Makefile.test
│       ├── docs/
│       │   └── design.md                # Detailed design doc
│       └── README.md                    # Task Manager docs
│
├── docs/                                # Documentation
│   ├── user-guide.md                    # End-user guide
│   ├── developer-guide.md               # Development guide
│   ├── api-reference.md                 # Component APIs
│   ├── proc-filesystem.md               # /proc reference
│   └── images/
│       └── architecture.png             # Architecture diagrams
│
├── tests/                               # Integration tests
│   ├── test-ding.sh                     # Functional tests for ding
│   ├── test-showip.sh                   # Functional tests for showip
│   ├── test-task-manager.cpp            # Unit tests for manager
│   ├── test-iso-boot.md                 # Manual ISO boot test guide
│   └── Makefile                         # Test runner
│
├── build/                               # Build artifacts (gitignored)
│   ├── bin/
│   │   ├── ding
│   │   ├── showip -> ../../../src/showip/showip.sh
│   │   └── task-manager
│   ├── iso/
│   │   └── dingo-os.iso                 # Final deliverable
│   └── logs/
│       └── build.log
│
├── scripts/                             # Utility scripts
│   ├── build.sh                         # Full build script
│   ├── build-iso.sh                     # ISO generation script
│   ├── test-all.sh                      # Run all tests
│   ├── clean.sh                         # Clean build artifacts
│   └── install-deps.sh                  # Install development dependencies
│
├── .gitignore                           # Git ignore rules
└── Makefile                             # Top-level Makefile
```

---

## 5. Build Pipeline

```
┌─────────────────────────────────────────────┐
│ 1. Development Setup                        │
│ - Install dependencies (gcc, python, etc)  │
│ - Clone repo / initialize                  │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 2. Compile Components                       │
│ - make -C src/task-manager                  │
│ - Validate ding.py syntax                   │
│ - Validate showip.sh syntax                 │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 3. Run Unit & Integration Tests             │
│ - Test each utility in isolation            │
│ - Verify /proc parsing                      │
│ - Check apt wrapper functionality           │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 4. Stage Binaries                           │
│ - Copy binaries to build/bin/               │
│ - Prepare Cubic configuration               │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 5. Generate ISO with Cubic                  │
│ - Load Ubuntu 22.04 LTS base                │
│ - Inject custom packages & utilities        │
│ - Run preseed installer                     │
│ - Build ISO image                           │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 6. Test ISO Boot                            │
│ - Boot in virtual machine                   │
│ - Verify utilities installed                │
│ - Run smoke tests                           │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│ 7. ISO Deliverable                          │
│ - build/iso/dingo-os.iso (ready for dist)  │
└─────────────────────────────────────────────┘
```

---

## 6. Technology Stack Details

| Layer | Tool/Language | Purpose | Notes |
|-------|---------------|---------|-------|
| ISO Generation | Cubic + Bash | Remaster Ubuntu | GUI tool, simplifies workflow |
| ding | Python 3.8+ | Package manager logic | Easy to maintain, good stdlib |
| ding Wrapper | Bash | System integration | Portable, direct shell access |
| showip | Bash | Network utilities | Lightweight, direct `/proc` parsing |
| Task Manager | C++ | Process management | Performance-critical, direct syscalls |
| Testing | Bash + C++ | Validation | Native unit tests for C++ |
| Build | Make | Compilation & automation | Standard Unix tool |
| Config | YAML | User preferences | Human-readable, Python-friendly |

---

## 7. /proc Filesystem Reference (Task Manager)

```
Key files used by Task Manager:

/proc/cpuinfo                   # CPU information
/proc/stat                      # Global CPU statistics
/proc/uptime                    # System uptime
/proc/meminfo                   # Memory statistics
/proc/loadavg                   # Load average
/proc/[pid]/stat                # Process statistics
/proc/[pid]/status              # Process status details
/proc/[pid]/cmdline             # Command line arguments
/proc/[pid]/cwd                 # Working directory
/proc/[pid]/exe                 # Executable path
/proc/[pid]/fd/                 # File descriptors
/proc/[pid]/maps                # Memory map
/proc/net/dev                   # Network device stats
```

---

## 8. API & Module Interfaces

### ding Module
```python
class DingPackageManager:
    def install(package: str) -> bool
    def remove(package: str) -> bool
    def update() -> bool
    def search(query: str) -> List[Package]
    def get_info(package: str) -> PackageInfo
    def parse_config(path: str) -> Config
```

### showip Module
```bash
showip [interface] [--detailed] [--json] [--dns]
# Returns: formatted network interface information
```

### Task Manager Module (C++)
```cpp
class ProcessManager {
    vector<Process> getAllProcesses();
    Process getProcessById(int pid);
    vector<Process> filterByName(string name);
    void killProcess(int pid);
    void pauseProcess(int pid);
    SystemStats getSystemStats();
};
```

---

## 9. Integration Points

```
┌─ Cubic (ISO generation) ─┐
│ - Reads cubic-config/    │
│ - Includes packages      │
│ - Injects utilities      │
└──────────┬───────────────┘
           │
    [Generated ISO]
           │
        ┌──┴──┐
        │     │
    ding  showip  task-manager
        │     │
        └─────┴── (All install to /usr/bin/ or /usr/local/bin/)
                  (Config to ~/.dingo/ or /etc/dingo/)
```

---

## 10. Security Considerations

- **ding wrapper**: Validates apt commands before execution; no shell injection
- **showip wrapper**: Read-only operations; no privilege escalation
- **Task Manager**: Process control requires user confirmation; respects process ownership
- **Configuration**: Config files in user home directory; readable/writable only by owner

---

## 11. Performance Targets

| Component | Target | Notes |
|-----------|--------|-------|
| ding | <2s for search | Acceptable shell wrapper latency |
| showip | <500ms | Read-only, should be fast |
| Task Manager | <100ms refresh | Acceptable for interactive UI |
| ISO Size | <3GB | Compact Ubuntu + utilities |

---

## 12. Deployment Checklist

- [ ] All source files compiled and tested
- [ ] Documentation complete and reviewed
- [ ] ISO successfully builds via Cubic
- [ ] ISO boots in VM without errors
- [ ] All utilities found in PATH and functional
- [ ] Utilities accept --help and --version flags
- [ ] Config files created with sensible defaults
- [ ] No hardcoded paths or dependencies
- [ ] LICENSE and attribution documented
