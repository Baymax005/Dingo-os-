# Dingo OS - Bucket Framework Specification

## Overview

The **Bucket Framework** reimagines Linux filesystem organization by introducing a Windows-like drive-letter architecture mapped to organized "buckets" on Linux.

Instead of navigating `/home/user/projects/...` and `/etc/...`, users reference:
```
D:/myproject/     # Data projects
E:/app.conf       # Configuration
S:/nginx/         # Services
T:/cache/         # Temporary files
```

---

## Core Concept

### Traditional Linux
```
/
├── home/
├── etc/
├── var/
├── opt/
└── srv/
```

### Dingo OS Buckets
```
D: → /mnt/dingo/data        (User data, projects)
E: → /mnt/dingo/etc         (Configuration)
S: → /mnt/dingo/services    (Services, daemons)
T: → /mnt/dingo/temp        (Temporary files)
W: → /mnt/dingo/workspace   (Development)
B: → /mnt/dingo/backups     (Backup storage)
L: → /mnt/dingo/logs        (System logs)
```

---

## Benefits

### For Users
- **Familiar** — Windows-like path structure
- **Organized** — Clear separation of concerns
- **Portable** — Easy to move buckets between systems
- **Intuitive** — Easy to understand what goes where

### For System
- **Isolated** — Easier permissions and backups per bucket
- **Scalable** — Can move buckets to different storage
- **Monitored** — Track usage per bucket
- **Optimizable** — Different filesystems per bucket

---

## Architecture

### Components

#### 1. Bucket Daemon (C++)
Central service managing bucket operations.

```cpp
class BucketDaemon {
public:
    // Mount/Unmount
    bool mount_bucket(const string& letter, const string& path);
    bool unmount_bucket(const string& letter);
    
    // Query
    string query_bucket_path(const string& letter);
    Bucket get_bucket_info(const string& letter);
    vector<Bucket> list_buckets();
    
    // Manage
    bool create_bucket(const string& letter, const Bucket& config);
    bool remove_bucket(const string& letter);
    
    // Monitor
    BucketStats get_stats(const string& letter);
    void watch_usage(const string& letter, const Callback& cb);
};
```

#### 2. Bucket CLI (Bash wrapper)
User-facing command interface.

```bash
# Mount/unmount
dingo-bucket mount D:/
dingo-bucket unmount D:

# Query
dingo-bucket path D:/myfile.txt      # → /mnt/dingo/data/myfile.txt
dingo-bucket exists D:/oldfile

# List and info
dingo-bucket list                    # Show all buckets
dingo-bucket info D:                 # Size, usage, permissions

# Manage
dingo-bucket create P: /path/to/projects
dingo-bucket remove P:

# Monitor
dingo-bucket usage D:                # Show disk usage
dingo-bucket watch T: --threshold 80%
```

#### 3. Bucket Daemon Configuration
```yaml
# /etc/dingo/bucket-daemon.conf

buckets:
  D:
    name: "Data"
    path: /mnt/dingo/data
    mounted: true
    permissions: 0755
    owner: dingo
    size-limit: 500G
    
  E:
    name: "Config"
    path: /mnt/dingo/etc
    mounted: true
    permissions: 0700
    owner: root
    size-limit: 10G
    
  S:
    name: "Services"
    path: /mnt/dingo/services
    mounted: true
    permissions: 0755
    owner: root
    size-limit: 100G
    
  T:
    name: "Temporary"
    path: /mnt/dingo/temp
    mounted: true
    permissions: 0777
    owner: root
    size-limit: 50G
    
  W:
    name: "Workspace"
    path: /mnt/dingo/workspace
    mounted: true
    permissions: 0755
    owner: dingo
    size-limit: 200G
    
  B:
    name: "Backups"
    path: /mnt/dingo/backups
    mounted: false
    permissions: 0700
    owner: root
    size-limit: 1T
    
  L:
    name: "Logs"
    path: /mnt/dingo/logs
    mounted: true
    permissions: 0755
    owner: root
    size-limit: 50G
```

---

## Usage Examples

### Basic Bucket Operations

```bash
# Mount a bucket
dingo-bucket mount D:
# Mounting D: (Data bucket)...
# ✓ Mounted at /mnt/dingo/data

# List all buckets
dingo-bucket list
# D:  Data         /mnt/dingo/data      [Mounted]  123.4 GB / 500 GB
# E:  Config       /mnt/dingo/etc       [Mounted]   45.2 MB / 10 GB
# S:  Services     /mnt/dingo/services  [Mounted]   234.5 GB / 100 GB
# T:  Temporary    /mnt/dingo/temp      [Mounted]    5.3 GB / 50 GB
# W:  Workspace    /mnt/dingo/workspace [Mounted]   78.9 GB / 200 GB

# Show bucket info
dingo-bucket info D:
# Bucket: D: (Data)
# Path: /mnt/dingo/data
# Status: Mounted
# Size: 123.4 GB / 500 GB (24.7%)
# Owner: dingo:dingo
# Permissions: 0755
```

### Path Resolution

```bash
# Query absolute path
dingo-bucket path D:/projects/myapp
# /mnt/dingo/data/projects/myapp

# Check if path exists
dingo-bucket exists D:/projects/oldapp
# ✓ Path exists
# Type: directory
# Size: 123 MB

# List bucket contents
dingo-bucket ls D:/
# projects/
# downloads/
# documents/
```

### Bucket Monitoring

```bash
# Show usage statistics
dingo-bucket usage
# Bucket Usage Summary:
# D:  123.4 GB / 500 GB   [████████░░░░░░░░░░] 24.7%
# E:   45.2 MB / 10 GB    [░░░░░░░░░░░░░░░░░░] 0.4%
# S:  234.5 GB / 100 GB   [████████████████░░] 234.5%⚠️
# T:    5.3 GB / 50 GB    [██░░░░░░░░░░░░░░░░] 10.6%

# Watch bucket in real-time
dingo-bucket watch D: --interval 5s
# Monitoring D: (refresh every 5s)...
# [Ctrl+C to stop]
```

### Bucket Administration

```bash
# Create new bucket
dingo-bucket create P: /path/to/projects
# ✓ Created bucket P: (Projects) at /path/to/projects

# Set size limit
dingo-bucket set-limit D: 1T

# Change permissions
dingo-bucket chmod D: 0755

# Change owner
dingo-bucket chown D: dingo:dingo

# Remove bucket (unmount + cleanup)
dingo-bucket remove B:
# ⚠️  This will unmount B: and remove /mnt/dingo/backups
# Continue? [y/N] n
```

---

## Integration with Other Tools

### ding Package Manager Integration

```bash
# Install to specific bucket
ding install --bucket S: nginx apache2

# List packages by bucket
ding list --bucket S:
```

### Task Manager Integration

```bash
# Monitor services in S: bucket
task-manager --filter S:/

# Show process resource usage per bucket
task-manager --bucket-stats
```

### dingo-audit Integration

```bash
# Audit specific bucket
dingo-audit --bucket S: --security

# Check bucket permissions
dingo-audit --bucket E: --permissions
```

---

## Implementation Details

### File Structure

```
/mnt/dingo/
├── data/              # D: User data
├── etc/               # E: Configuration
├── services/          # S: Services/apps
├── temp/              # T: Temporary files
├── workspace/         # W: Development
├── backups/           # B: Backups
├── logs/              # L: System logs
└── .bucket-metadata/  # Daemon config & metadata
    ├── daemon.conf
    ├── bucket-registry.json
    └── mount-state.json
```

### Daemon Socket Communication

```
/var/run/dingo/bucket-daemon.sock

Commands:
- mount <letter> <path>
- unmount <letter>
- query_path <letter>:<path>
- list_buckets
- get_stats <letter>
- create <letter> <config>
- remove <letter>
```

### Symbolic Link Resolution

```bash
# Behind the scenes:
# D: → symlink to /mnt/dingo/data
# E: → symlink to /mnt/dingo/etc
# S: → symlink to /mnt/dingo/services

# In shell:
cd D:/
# Resolved to: cd /mnt/dingo/data/
```

---

## Security Model

### Permissions

- **D:** (Data) — User-writable, user-readable
- **E:** (Config) — Root-only
- **S:** (Services) — Daemon-writable, world-readable
- **T:** (Temp) — World-writable
- **W:** (Workspace) — Developer-writable
- **B:** (Backups) — Root-only
- **L:** (Logs) — Daemon-writable, admin-readable

### Isolation

- Buckets can be on separate filesystems
- Different storage devices possible
- Per-bucket backup/restore
- Quota enforcement per bucket

---

## Performance

| Operation | Target Time |
|-----------|-------------|
| Mount bucket | <100ms |
| Path query | <1ms |
| List buckets | <50ms |
| Usage stats | <500ms |
| Daemon startup | <1s |

---

## Migration Path

### Phase 1: Opt-in
- Users can mount individual buckets
- Backward compatible with /mnt paths
- No forced migration

### Phase 2: Guided Migration
- Tools help move existing data to buckets
- Documentation for migration
- Automated scripts

### Phase 3: Standard
- New installs use buckets by default
- Legacy paths still supported
- Advanced features utilize buckets

---

## Future Enhancements

- Remote bucket mounting (NFS, SFTP)
- Cloud bucket integration (S3, etc.)
- Bucket replication and synchronization
- Encryption per bucket
- Advanced quota management
- Bucket snapshots and versioning

---

## Technical Stack

- **Daemon**: C++ with D-Bus or custom socket protocol
- **CLI**: Bash wrapper around daemon communication
- **Storage**: Linux ext4/btrfs/xfs with quotas
- **Communication**: Unix sockets or D-Bus
- **Monitoring**: Real-time inotify integration

---

## Example Use Cases

### Developer Workflow
```bash
# All project files in one bucket
D:/projects/backend/
D:/projects/frontend/
D:/projects/devops/

# Clean separation from system
E:/app-configs/
S:/app-services/
```

### System Administration
```bash
# Services isolated
S:/nginx/
S:/postgresql/
S:/redis/

# Configs secured
E:/nginx.conf
E:/postgresql.conf

# Logs organized
L:/nginx/
L:/postgresql/
```

### Backup Strategy
```bash
# Selective backups by bucket
backup D: → backup-data-2024-01-15.tar
backup E: → backup-config-2024-01-15.tar
backup S: → backup-services-2024-01-15.tar
```

---

## Conclusion

The Bucket Framework brings Windows-familiar organization to Linux while maintaining security and flexibility. It enables better resource management, simpler backups, and more intuitive filesystem navigation for all users.
