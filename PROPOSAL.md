# Dingo OS - Project Proposal

## 1. Executive Summary
Create a custom, user-friendly Linux distribution (Dingo OS) based on Ubuntu, featuring simplified system utilities and a custom process manager built from scratch. The project demonstrates kernel/process management principles while delivering a tangible, bootable OS.

---

## 2. Project Goals & Objectives

### Primary Goals
- Develop a remastered Ubuntu distribution with a cohesive, simplified user interface
- Build three core user-space utilities that demonstrate system programming concepts
- Create a bootable ISO deployable on bare metal or VMs
- Learn practical Linux kernel concepts (process management, `/proc` filesystem, memory management)

### Learning Outcomes
- Understanding of Linux process hierarchy and system state management
- Experience with system-level programming (C++/Python interfacing with kernel abstractions)
- Knowledge of package management architecture and CLI design
- Practical ISO generation and bootable system creation

---

## 3. Version Status

### v1 - COMPLETE ✅ (Bootable ISO Ready)

**Completed Deliverables**:
- ✅ Custom Task Manager (C++ process monitor)
- ✅ showip (network utilities wrapper)
- ✅ ding (basic apt wrapper)
- ✅ Cubic ISO configuration
- ✅ Ubuntu 22.04 LTS bootable ISO
- ✅ All utilities pre-installed and tested
- ✅ Custom welcome message on boot
- ✅ Full documentation

**v1 Features**:
- Task Manager: Process listing, filtering, killing
- showip: Network interface display
- ding: Simplified apt commands
- ISO: Boots successfully on VM/bare metal

---

### v2 - IN DEVELOPMENT 🚀 (1.5 Weeks)

**Planned Enhancements**:

#### Component 1: ding v2 (Package Manager)
- Smart caching (cache frequent searches)
- Repository management (add/remove PPAs)
- Basic plugin system
- Backward compatible with v1

#### Component 2: dingo-audit (Security Scanner)
- Quick vulnerability scanning (<30s)
- System audit (deep security check)
- Network enumeration
- Forensic reporting
- Export to file

**What's Next (Post v2)**:
- Deferred to v3+: Advanced plugins, dingo-forensics, dingo-monitor
- Future roadmap: Extended tooling, system monitoring, advanced security

---

## 4. Scope & Deliverables (v1 MVP - COMPLETED)

### Core Deliverables (MVP - Must Have)
1. **Custom Task Manager** - Process Monitor (MVP Version)
   - Parse `/proc/[pid]/stat` for process info
   - Display running processes (PID, name, memory, CPU state)
   - **Essential Feature**: Kill process (with user confirmation)
   - No advanced features (pause, resume) - cut for time
   - CLI output (simple table, no fancy UI)

2. **showip** - Network Utilities Wrapper (Basic)
   - Wrap `ip addr show` with cleaner output
   - Display interface names and IP addresses
   - No DNS, routing, or JSON output for MVP

3. **Bootable ISO**
   - Ubuntu 22.04 LTS base (via Cubic)
   - Task Manager + showip pre-installed
   - Custom boot configuration
   - Ready for demo

### Optional Deliverables (If Time Permits)
- `ding` package manager wrapper (lower priority - can explain architecture without working code)
- Task Manager resource monitoring (cpu_percent, memory details)
- Interactive UI for Task Manager (basic table is fine)

### Out of Scope (Intentionally Cut for Time)
- Full test suite (spot-check only)
- Advanced Task Manager features (pause, resume, priority)
- Comprehensive documentation (GitHub README + 2-page summary only)
- ISO optimization or advanced customization
- Package repository hosting
- Configuration file system (hardcode defaults)

---

## 4. Technical Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Base OS | Ubuntu 22.04 LTS | Stable kernel + package ecosystem |
| ISO Generation | Ubuntu Cubic | Graphical remastering tool, streamlined workflow |
| ding | Bash + Python | Easy apt wrapper, CLI development |
| showip | Bash | Lightweight, direct command wrapping |
| Task Manager | C++ or Python | Direct `/proc` parsing, performance considerations |
| Database/Config | YAML/JSON | Human-readable configuration |

---

## 5. Development Phases (1-Week MVP Timeline)

### Phase 1: Foundation & Setup (Day 1 - ~4 hours)
- [ ] Set up Cubic ReMaster environment on Windows/VM
- [ ] Create project repository structure
- [ ] Set up development VM for testing
- [ ] **SKIP full architecture docs** (have basic plan)

### Phase 2: Task Manager MVP (Days 1-3 - ~16 hours)
**Priority: This is the showpiece**
- [ ] Design basic `/proc` filesystem parser (C++)
- [ ] Implement process listing by reading `/proc/[pid]/stat`
- [ ] Implement process filtering by name
- [ ] Basic display (table format, no fancy UI needed)
- [ ] Process kill functionality (one working feature)
- [ ] Compile & test in isolation

### Phase 3: Simple Utilities (Days 2-3 - ~8 hours)
**Bare-minimum versions**
- [ ] `showip` - Simple shell script wrapping `ip addr` 
  - Just displays interfaces cleanly, no advanced features
- [ ] `ding` wrapper - OPTIONAL if time permits
  - If skipped: explain why in docs and focus on Task Manager

### Phase 4: Integration & ISO (Days 4-5 - ~8 hours)
- [ ] Integrate Task Manager + showip into Cubic config
- [ ] Test ISO build (1-2 iterations max)
- [ ] Boot test in VM
- [ ] Create quick install/usage doc

### Phase 5: Polish & Live Demo (Days 6-7 - ~6 hours)
- [ ] Create demo script showing Task Manager working
- [ ] Write 2-page project summary (not full docs)
- [ ] Final ISO test
- [ ] Git commit with clear README

---

## 6. Directory Structure (Initial)

```
dingo-os/
├── PROPOSAL.md                  # This file
├── ARCHITECTURE.md              # System design & structure
├── README.md                    # Getting started guide
├── cubic-config/                # Cubic remastering configuration
│   ├── preseed.cfg              # Ubuntu installation settings
│   └── custom-packages.list     # Package list
├── src/                         # Source code
│   ├── ding/                    # Package manager wrapper
│   │   ├── ding.py
│   │   ├── ding.sh
│   │   └── config.yaml
│   ├── showip/                  # Network utilities wrapper
│   │   ├── showip.sh
│   │   └── README.md
│   └── task-manager/            # Process manager
│       ├── task-manager.cpp     # C++ implementation
│       ├── task-manager.h
│       ├── Makefile
│       └── tests/
├── docs/                        # Documentation
│   ├── user-guide.md
│   ├── developer-guide.md
│   └── architecture-diagrams.md
├── tests/                       # Testing
│   ├── test-ding.sh
│   ├── test-showip.sh
│   └── test-task-manager.cpp
└── build/                       # Build artifacts (ISO, binaries)
```

---

## 7. Success Criteria (MVP)

- [ ] ISO builds without errors
- [ ] Task Manager runs and displays at least 5 processes correctly
- [ ] Task Manager successfully kills a process (with confirmation)
- [ ] showip displays network interfaces cleanly
- [ ] Both utilities installed in ISO and runnable from PATH
- [ ] ISO boots cleanly in VM
- [ ] 5-10 minute live demo works (doesn't crash)
- [ ] README explains what was built and why
- [ ] Source code is readable and has basic comments
- [ ] Git history shows incremental progress (not one giant commit)

---

## 8. Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Cubic tool incompatibility | Medium | Use well-documented LTS version; test early |
| `/proc` parsing edge cases | Medium | Comprehensive testing on multiple kernel versions |
| Package dependency issues | Medium | Pin package versions; document requirements |
| ISO build time (feedback loops) | Low | Automate testing; use snapshot VMs |
| Scope creep | High | Strictly enforce deliverable list; document deferred features |

---

## 9. Resource Requirements

- **Hardware**: Development machine (Linux preferred), test VM
- **Software**: Ubuntu Cubic, GCC/G++, Python 3.8+, Bash
- **Time**: ~6 weeks for full development cycle (part-time friendly)
- **Knowledge**: Linux basics, shell scripting, process management concepts

---

## 10. Next Steps

1. Review and approve this proposal
2. Create ARCHITECTURE.md with detailed system design
3. Set up Cubic environment and test basic ISO generation
4. Begin Phase 1: Foundation & Setup
