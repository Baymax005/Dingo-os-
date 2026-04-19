# Dingo OS - ding Package Manager v2 Specification

## Overview

`ding` is Dingo OS's custom package manager wrapper built on top of `apt`. v2 enhances it with:
- Plugin system for extensibility
- Repository management
- Smart caching
- Bucket framework integration
- Enhanced filtering and search

---

## v2 Features

### 1. Plugin System

**Install plugins**:
```bash
ding plugin install security-scanner
ding plugin install auto-update
```

**Manage plugins**:
```bash
ding plugin list                 # Show all plugins
ding plugin info security-scanner
ding plugin enable/disable NAME
ding plugin remove NAME
```

**Plugin directory**: `~/.dingo/plugins/`

### 2. Repository Management

**Add repositories**:
```bash
ding repo add ubuntu-security ppa:ubuntu/security
ding repo add custom https://repo.example.com/deb
```

**List repositories**:
```bash
ding repo list                   # Show all repos
ding repo list --enabled         # Show active repos
```

**Remove repositories**:
```bash
ding repo remove ubuntu-security
```

### 3. Smart Caching

**Cache operations**:
```bash
ding cache-stats                 # Show cache size
ding cache-clean                 # Clear old cache
ding cache-rebuild               # Rebuild cache index
```

**Auto-cache features**:
- Automatic cleanup of old caches
- Predictive caching for frequent searches
- Fast index rebuilding

### 4. Dependency Analysis

**Check dependencies**:
```bash
ding depends gcc                 # Show what gcc needs
ding depends-on gcc              # Show what needs gcc
ding depends-tree gcc            # Tree view
```

### 5. Advanced Search

**Enhanced search**:
```bash
ding search --category devel gcc           # Search by category
ding search --installed curl               # Search installed packages
ding search --upgradable                   # Find upgradable packages
ding search --size >10M                    # Search by size
ding search --recent                       # Recently published
```

### 6. Configuration Management

**Config files**:
```bash
ding config set auto-update true
ding config get auto-update
ding config list                 # Show all settings
ding config reset                # Reset to defaults
```

**Config locations**:
- User: `~/.dingo/ding.conf`
- System: `/etc/dingo/ding.conf`
- Plugins: `~/.dingo/plugins/config/`

---

## Architecture

```
┌─────────────────────────────────────┐
│      ding CLI (v2)                  │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Command Parser & Validator  │   │
│  └──────────────┬──────────────┘   │
│                 │                   │
│  ┌──────────────▼──────────────┐   │
│  │ Plugin System               │   │
│  │ • Load plugins              │   │
│  │ • Execute hooks             │   │
│  └──────────────┬──────────────┘   │
│                 │                   │
│  ┌──────────────▼──────────────┐   │
│  │ Core Operations             │   │
│  │ • install/remove            │   │
│  │ • search/filter             │   │
│  │ • list/show                 │   │
│  └──────────────┬──────────────┘   │
│                 │                   │
│  ┌──────────────▼──────────────┐   │
│  │ Cache Manager               │   │
│  │ • Store queries             │   │
│  │ • Manage index              │   │
│  └──────────────┬──────────────┘   │
│                 │                   │
│  ┌──────────────▼──────────────┐   │
│  │ Repository Manager          │   │
│  │ • Add/remove repos          │   │
│  │ • Update indexes            │   │
│  └──────────────┬──────────────┘   │
│                 │                   │
│  ┌──────────────▼──────────────┐   │
│  │ Bucket Framework Interface  │   │
│  │ • Query bucket paths        │   │
│  │ • Mount/unmount buckets     │   │
│  └──────────────┬──────────────┘   │
│                 │                   │
│  ┌──────────────▼──────────────┐   │
│  │ apt Executor                │   │
│  │ • Run apt commands          │   │
│  │ • Parse output              │   │
│  │ • Error handling            │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Plugin System
1. Create plugin loader
2. Define plugin interface
3. Build first plugins (security-scanner, auto-update)
4. Add plugin marketplace

### Phase 2: Repository Management
1. Add repo add/remove/list
2. Create repo config storage
3. PPA support
4. Custom repo authentication

### Phase 3: Smart Caching
1. Implement cache storage
2. Add cache management commands
3. Integrate with searches
4. Performance monitoring

### Phase 4: Bucket Integration
1. Add bucket parameter to install
2. Create bucket-aware package listing
3. Cross-bucket dependency resolution
4. Bucket-specific configurations

---

## Plugin Development Guide

### Create a Plugin

```python
# ~/.dingo/plugins/my-plugin.py

from dingplugin import DingPlugin

class MyPlugin(DingPlugin):
    name = "my-plugin"
    version = "1.0"
    description = "My custom plugin"
    
    def on_install(self, package):
        """Called after package install"""
        print(f"Installed: {package}")
    
    def on_remove(self, package):
        """Called after package remove"""
        print(f"Removed: {package}")
    
    def custom_command(self, args):
        """Custom ding subcommand"""
        return 0

# Register plugin
__plugin__ = MyPlugin()
```

### Plugin Hooks

- `on_install(package)` — After install
- `on_remove(package)` — After remove
- `on_search(query)` — Before search
- `on_upgrade()` — After upgrade
- `on_config_change(key, value)` — Config changed

---

## Configuration File Format

```yaml
# ~/.dingo/ding.conf

# Auto-update settings
auto-update:
  enabled: true
  interval: 24h
  
# Cache settings
cache:
  max-size: 500M
  auto-clean: true
  
# Repository settings
repositories:
  - name: ubuntu-main
    enabled: true
  - name: ubuntu-security
    enabled: true

# Bucket defaults
buckets:
  install-default: S:
  cache-bucket: T:
  
# Plugins
plugins:
  enabled:
    - security-scanner
    - auto-update
  disabled: []
```

---

## Usage Examples

### Install from specific repo
```bash
ding install --repo ubuntu-security openssl
```

### Search with advanced filters
```bash
ding search --category dev --installed --upgradable
```

### Check dependencies tree
```bash
ding depends-tree gcc
# gcc
# ├── build-essential
# ├── binutils
# └── g++
#     ├── cpp
#     └── gcc
```

### Install to services bucket
```bash
ding install --bucket S: nginx apache2 postgresql
```

### Manage cache
```bash
ding cache-stats
# Cache statistics:
# Total size: 245 MB
# Packages cached: 1,234
# Last updated: 2 hours ago

ding cache-clean --older-than 7d
```

### Run plugin command
```bash
ding security-scanner scan
# Security scanning...
# Found 3 potential updates
# 5 end-of-life packages
```

---

## Backward Compatibility

- All v1 commands still work
- v1 syntax mapped to v2 internally
- Configuration auto-migrates
- No breaking changes

---

## Performance

- Search: <500ms (with cache)
- Install: <2s wrapper overhead
- Plugin load: <100ms
- Cache rebuild: <10s

---

## Security

- Plugin signature verification
- Repository signing validation
- Cache integrity checking
- Dependency audit for CVEs
- Secure plugin marketplace

---

## Future Enhancements (Beyond v2)

- Machine learning for dependency prediction
- Graphical package manager UI
- Collaborative plugin marketplace
- Package attestation and provenance
- Container integration
