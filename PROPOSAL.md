# Dingo OS - Custom Linux Distribution
## Final Semester Project Proposal

---

## 1. Executive Summary

**Dingo OS** is a custom Linux distribution built on Ubuntu 22.04 LTS, designed to demonstrate key operating system concepts through practical implementation. This project involves creating a remastered bootable ISO with custom system utilities (process manager, network utilities, package manager, security auditor) that interact directly with kernel abstractions like the `/proc` filesystem, memory management, and process scheduling.

The project showcases **three core OS competencies**:
1. **Process Management** — Building a custom task manager that reads and manipulates process state
2. **System Programming** — Interfacing with kernel abstractions through `/proc`, `/sys`, and system calls
3. **System Administration** — Creating a distribution, managing packages, and configuring bootable systems

**Deliverable**: A fully bootable 5.2GB ISO demonstrating all concepts, deployable on VirtualBox, VMware, or bare metal.

---

## 2. What We're Making

### High-Level Overview

Dingo OS is a **remastered Ubuntu distribution** with four integrated system utilities running as user-space programs:

| Component | Purpose | OS Concept |
|-----------|---------|-----------|
| **Task Manager** | Process monitoring and control | Process management, `/proc` filesystem |
| **showip** | Network interface information | Network syscalls, device drivers |
| **ding v2** | Enhanced package manager | Dependency resolution, package repositories |
| **dingo-audit** | Security scanner | Privilege escalation, permissions, open ports |

### What Makes It Different from Stock Ubuntu?

- ✅ **Lightweight XFCE desktop** instead of heavy GNOME (demonstrates OS resource optimization)
- ✅ **Integrated custom utilities** that interact with kernel abstractions
- ✅ **Cyberpunk aesthetic** with custom terminal colors and branding
- ✅ **Security-focused tools** built from scratch (not just wrappers)
- ✅ **Educational value** — every component teaches real OS concepts

---

## 3. Core OS Concepts Demonstrated

### 3.1 Process Management (Task Manager)

**What it does**: Lists, filters, and terminates running processes

**OS Concepts Covered**:
- **Process State Reading**: Parses `/proc/[pid]/stat` to read process state (running, sleeping, zombie)
- **Memory Management**: Extracts RSS (resident set size) to show process memory usage
- **Signals & IPC**: Implements `SIGKILL` signal handling for process termination
- **Process Hierarchy**: Displays parent-child relationships (PPID)
- **Scheduling**: Shows thread count and CPU state information

**Code Example**:
```cpp
// Reads /proc/[pid]/stat to extract process information
// Demonstrates: file I/O, parsing kernel abstractions, resource tracking
pid_t pid = stoi(entry->d_name);
string stat_file = "/proc/" + to_string(pid) + "/stat";
ifstream file(stat_file);
// Parse stat format: pid (comm) state ppid pgrp session tty_nr tpgid flags ...
```

---

### 3.2 System Programming (Network Utilities)

**What it does**: Displays network interfaces and IP addresses

**OS Concepts Covered**:
- **Network Stack**: Reading from `/sys/class/net` to enumerate interfaces
- **Device Drivers**: Understanding how OS abstracts hardware as files
- **System Calls**: Using `ioctl()` and socket syscalls to query network state
- **Character Devices**: Interaction with network device files in `/dev`

---

### 3.3 Package Management (ding v2)

**What it does**: Smart wrapper around apt with caching and repository management

**OS Concepts Covered**:
- **Dependency Resolution**: Understanding how apt solves package conflicts
- **Repository Management**: Adding/removing PPAs, managing `/etc/apt/sources.list`
- **Caching Strategy**: Implementing LRU cache for frequently accessed packages
- **Plugin Architecture**: Dynamic loading of modules (Python `importlib`)

---

### 3.4 Security & System Auditing (dingo-audit)

**What it does**: Scans for vulnerabilities, open ports, and permission issues

**OS Concepts Covered**:
- **Permissions & Access Control**: Reading file permissions, checking sudoers
- **Network Security**: Scanning open ports using `netstat`, checking listening services
- **Privilege Escalation**: Identifying vulnerable sudoers configurations
- **System Call Tracing**: Monitoring processes and system activity

---

## 4. Advantages

### 4.1 Educational Value

| Advantage | Why It Matters |
|-----------|---|
| **Hands-on Learning** | Students write actual OS concepts (not just theory) |
| **Real-world Skills** | Creating distributions is a sought skill in DevOps/Linux communities |
| **Visual Demonstration** | Bootable ISO proves concepts work in practice |
| **Full Stack Understanding** | From kernel APIs to user interface |

### 4.2 Technical Advantages

| Advantage | Benefit |
|-----------|---------|
| **Reproducibility** | All 7 phases of ISO customization are documented and automatable |
| **Modularity** | Each utility is independent, can be tested separately |
| **No External Dependencies** | All tools use only standard Linux APIs (no external libraries) |
| **Performance Validation** | Can measure real system impact (boot time, memory usage, process overhead) |
| **Extensibility** | Easy to add new utilities (dingo-audit, dingo-forensics, etc.) |

### 4.3 Practical Advantages

| Advantage | Application |
|-----------|---|
| **Bootable ISO** | Can be deployed immediately on any system |
| **Version Control** | Full git history showing iterative development |
| **Documentation** | Complete guides for reproduction and extension |
| **Open Source** | Licensed under MIT, can be shared with others |

---

## 5. Features

### v1 Features (COMPLETED ✅)

#### 1. Custom Task Manager (C++)
```bash
task-manager              # List all processes
task-manager --filter bash        # Filter by name
task-manager --kill <PID>         # Kill process (with confirmation)
task-manager --help               # Show help
```
- ✅ Process listing (PID, name, state, memory, threads)
- ✅ Filtering by process name
- ✅ Process termination with user confirmation
- ✅ Memory and CPU state display
- ✅ Colored terminal output

#### 2. Network Utilities (Bash)
```bash
showip                    # Show all interfaces
showip eth0               # Show specific interface
showip --help             # Show help
```
- ✅ Display active network interfaces
- ✅ Show IPv4 and IPv6 addresses
- ✅ Network device statistics
- ✅ Clean, readable formatting

#### 3. Bootable ISO
- ✅ Ubuntu 22.04 LTS base
- ✅ XFCE4 + LightDM desktop
- ✅ All utilities pre-installed
- ✅ Custom boot configuration
- ✅ 5.2GB optimized size

---

### v2 Features (COMPLETED ✅)

#### 4. Enhanced Package Manager (ding v2)
```bash
ding cache-stats          # Show cache usage
ding repo add ubuntu-security ppa:ubuntu/security
ding repo list            # List active repositories
ding plugin list          # List available plugins
```
- ✅ Smart caching (100ms lookup vs 2-3s uncached)
- ✅ Repository management (add/remove PPAs)
- ✅ Basic plugin system (extensible)
- ✅ Backward compatible with apt

#### 5. Security Auditor (dingo-audit)
```bash
dingo-audit --quick       # Fast scan (30s)
dingo-audit --system      # Deep system audit (5m)
dingo-audit --network     # Network enumeration
dingo-audit --all         # Complete scan (10m)
```
- ✅ Open port scanning
- ✅ Service vulnerability checking
- ✅ File permission audit
- ✅ User accounts & sudoers analysis
- ✅ Export to file functionality

---

## 6. OS Curriculum Relevance

### Course Concepts Addressed

| OS Concept | Dingo OS Implementation |
|-----------|---|
| **Process Management** | Task manager reads `/proc/[pid]/stat`, demonstrates scheduling state |
| **Memory Management** | Task manager displays RSS, page faults, memory pressure |
| **File Systems** | All utilities interact with `/proc`, `/sys`, `/dev` virtual filesystems |
| **System Calls** | Uses `open()`, `read()`, `ioctl()`, `kill()`, `socket()` |
| **Signals** | Process termination uses SIGKILL signal handling |
| **Concurrency** | Handles multiple process reads simultaneously |
| **User/Kernel Space** | Clear boundary between user utilities and kernel abstractions |
| **Permissions & Security** | dingo-audit checks ACLs, sudoers, and privilege escalation |
| **Bootloader & Kernel** | Custom boot parameters, grub configuration |
| **Package Management** | ding demonstrates dependency resolution concepts |

### Learning Path

1. **Beginner**: Run the ISO, observe what each utility does
2. **Intermediate**: Read source code, understand `/proc` parsing
3. **Advanced**: Modify utilities, add new features, rebuild ISO
4. **Expert**: Create custom kernel modules, optimize syscall usage

---

## 7. Disadvantages & Limitations

### 7.1 Technical Limitations

| Limitation | Why It Exists | Impact |
|-----------|---|---|
| **User-space Only** | Creating kernel modules is beyond scope; /proc APIs sufficient | Cannot implement advanced scheduling or memory management |
| **Single-threaded Task Manager** | Simpler implementation, still demonstrates concepts | May lag with 1000+ processes |
| **Limited Network Info** | `showip` only displays interfaces, not routing tables | Doesn't show full network topology |
| **No GUI Dashboard** | CLI is simpler; learning focus on system calls, not UI | Can't visualize process hierarchy graphically |
| **Bash Security Tools** | Easier to write; not as performant as C | `dingo-audit` takes ~5 minutes for full scan |

### 7.2 Practical Limitations

| Limitation | Why It Exists | Workaround |
|-----------|---|---|
| **Requires Linux VM/Host** | Project is Linux-specific | Use VirtualBox, WSL, or native Linux |
| **5.2GB ISO Download** | Full distribution includes base OS | Can use minimal ISO (~1GB) with utilities installed separately |
| **Manual Testing** | No automated test suite (time constraint) | Can be added as post-semester enhancement |
| **Ubuntu-specific** | Built on Ubuntu 22.04 LTS | Concepts transferable to other distros (Debian, Fedora, etc.) |

### 7.3 Scope Limitations (Intentional)

| Feature | Status | Reasoning |
|---------|--------|-----------|
| Kernel Modules | ❌ Out of Scope | Requires kernel headers, compilation; 1-2 weeks work |
| Advanced Plugins | ❌ Deferred to v3 | Requires robust error handling, testing |
| dingo-forensics | ❌ Deferred to v3 | Deep system inspection, forensic analysis |
| Custom Installer | ❌ Deferred to v3 | Would require Calamares framework learning |
| Real-time Monitoring | ❌ Out of Scope | Would need event-based I/O, system tracing |

---

## 8. Technical Architecture

### System Layers

```
┌─────────────────────────────────────────┐
│     User Applications                   │
│  (task-manager, showip, ding, audit)   │
├─────────────────────────────────────────┤
│     System Libraries (libc, glibc)      │
│  (provides system call wrappers)        │
├─────────────────────────────────────────┤
│     System Call Interface               │
│  (open, read, ioctl, kill, socket)     │
├─────────────────────────────────────────┤
│     Kernel (Linux 5.15)                 │
│  (/proc, /sys, device drivers)         │
├─────────────────────────────────────────┤
│     Hardware                            │
│  (CPU, Memory, Network Interface)       │
└─────────────────────────────────────────┘
```

### Component Interaction

```
Task Manager ──reads──> /proc/[pid]/stat ──kernel─data──> Process State
                       /proc/meminfo       from scheduler
                       /proc/[pid]/status

showip ───queries──> /sys/class/net ──driver──> Network Interfaces
                     /proc/net/dev   from NIC

ding v2 ────parses──> /etc/apt/sources.list ──manages──> Package Lists
                      ~/.dingo/cache            repos

dingo-audit ─scans──> /proc/net/tcp ──checks──> Security Posture
                      /proc/[pid]/limits
                      /etc/sudoers
                      /proc/sys/kernel/*
```

---

## 9. Development Approach

### Iterative Development

| Phase | Duration | Focus | Deliverable |
|-------|----------|-------|---|
| **Phase 1** | Week 1-2 | Task Manager (C++) | Process listing working |
| **Phase 2** | Week 3 | showip + ding wrapper | Network display, package manager |
| **Phase 3** | Week 4-5 | ISO Creation & Testing | Bootable distribution |
| **Phase 4** | Week 5-6 | v2 Enhancements | Caching, audit tools |
| **Phase 5** | Week 6+ | Documentation & Polish | Final submission |

### Code Quality Standards

- ✅ **Comments** — Explain OS concepts, not obvious code
- ✅ **Modularity** — Each utility independent and testable
- ✅ **Error Handling** — Graceful failures for missing `/proc` entries
- ✅ **Performance** — <100ms for task listing, <1s for scans
- ✅ **Documentation** — README, guides, and inline technical notes

---

## 10. Deliverables

### Primary Deliverable
- ✅ **Bootable ISO** (5.2GB) with all utilities pre-installed
- ✅ **Full Source Code** (C++, Python, Bash) with comments
- ✅ **Complete Documentation**:
  - ISO_CUSTOMIZATIONS.md (7 phases)
  - README.md (quick start)
  - ARCHITECTURE.md (system design)
  - User guides for each utility

### Secondary Deliverables
- ✅ **Git Repository** with clear commit history
- ✅ **MIT License** for open-source distribution
- ✅ **Working Demos** (video or live demonstration)
- ✅ **Build Scripts** for reproducibility

---

## 11. Evaluation Criteria

### Technical Completeness
- [ ] Task manager compiles and runs without errors
- [ ] All utilities functional and tested
- [ ] ISO boots successfully on VM and/or bare metal
- [ ] Utilities installed in PATH and accessible
- [ ] Process termination works safely
- [ ] Code handles edge cases (missing files, permissions)

### OS Competency
- [ ] Clear explanation of `/proc` filesystem usage
- [ ] Demonstrates understanding of process scheduling
- [ ] Shows system call implementation
- [ ] Explains memory management concepts
- [ ] Connects code to course material

### Presentation Quality
- [ ] Clean, readable source code
- [ ] Comprehensive documentation
- [ ] Professional commit messages
- [ ] Organized GitHub repository
- [ ] Working live demonstration

### Innovation & Extension
- [ ] Custom branding and aesthetic
- [ ] Additional features beyond requirements
- [ ] Performance optimizations
- [ ] Security considerations
- [ ] Future roadmap (v3 plans)

---

## 12. Risk Analysis & Mitigation

| Risk | Probability | Severity | Mitigation |
|------|-------------|----------|-----------|
| Cubic tool compatibility | Low | High | Test on target kernel version early |
| `/proc` parsing edge cases | Medium | Medium | Comprehensive error handling, test on multiple VMs |
| Bootloader configuration | Low | High | Follow Cubic documentation, test early |
| Scope creep | Medium | High | Strict feature list, defer v3 features |
| Performance issues | Low | Medium | Profile early, optimize hotspots |
| Time management | Medium | Medium | Weekly milestones, daily tracking |

---

## 13. Conclusion

Dingo OS is a **comprehensive OS course project** that bridges theory and practice. By building a custom Linux distribution with system utilities that directly interact with kernel abstractions, students gain:

✅ **Practical OS knowledge** — Not just exams, but working code  
✅ **System programming skills** — Real-world Linux development  
✅ **Software engineering practices** — Version control, documentation, testing  
✅ **Professional portfolio piece** — Demonstrates competency to employers  

The project is **challenging but achievable** in a semester, with clear phases and fallback options if time constraints arise. The resulting bootable ISO is a tangible artifact proving mastery of OS concepts.

---

## 14. Next Steps

1. **Submit this proposal** for instructor approval
2. **Receive feedback** on scope and timeline
3. **Begin Phase 1** (setup and foundation)
4. **Track progress** with weekly milestones
5. **Deliver final ISO** with complete documentation
6. **Present findings** in final seminar/presentation

---

## Appendix A: Related OS Concepts

**Linux Process Model**: Understanding how processes are created, scheduled, and terminated using fork/exec model, demonstrated through task manager.

**Virtual Filesystems**: The `/proc` and `/sys` filesystems provide a window into kernel state, used extensively in all utilities.

**System Call Interface**: Bridge between user-space and kernel-space, exemplified in process management and network queries.

**User/Kernel Space Separation**: Clear boundaries maintained throughout—all utilities are user-space, privileged operations use kernel-mediated APIs.

**Package Management Philosophy**: Dependency resolution, version management, and repository architecture demonstrated through ding v2.

---

## Appendix B: References

- **Linux Kernel Documentation** — `/proc` filesystem, process management
- **Ubuntu Documentation** — Custom distribution creation
- **POSIX Standard** — System call specifications
- **Computer Systems Organization Course Materials** — Process models, memory hierarchy
- **Security Best Practices** — Permission models, privilege escalation

---

**Project Status**: ✅ v2 COMPLETE | **Last Updated**: 2026-04-20 | **Team**: Muhammad Ali