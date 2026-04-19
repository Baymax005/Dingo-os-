# ding v2 - Enhanced Package Manager

**ding** is Dingo OS's custom package manager wrapper built on apt with smart features.

## v2 Features

### 1. Smart Caching

Cache frequently used searches and package info for faster lookups.

```bash
# Show cache statistics
ding cache-stats
# Cache statistics:
# Total size: 45 MB
# Packages cached: 234
# Last updated: 2 hours ago

# Clear cache
ding cache-clean
# Cache cleared. Freed 45 MB

# Rebuild cache index
ding cache-rebuild
# Rebuilding cache... done!
```

### 2. Repository Management

Easily add, remove, and manage package repositories (PPAs).

```bash
# Add a repository
ding repo add ubuntu-security ppa:ubuntu/security

# List all repositories
ding repo list
# ubuntu (default)
# ubuntu-security (enabled)
# ubuntu-updates (disabled)

# Remove a repository
ding repo remove ubuntu-security

# Enable/disable repository
ding repo enable ubuntu-security
ding repo disable ubuntu-security
```

### 3. Basic Plugin System

Extend ding with custom commands through plugins.

```bash
# List available plugins
ding plugin list
# custom-search
# auto-update

# Load a plugin
ding plugin load my-commands.py

# Execute plugin command
ding plugin execute custom-search python3
```

### 4. Regular Operations (Same as v1)

All v1 commands still work:

```bash
# Install
ding install nginx

# Search
ding search python

# Update
ding update

# Upgrade
ding upgrade

# Remove
ding remove old-package

# Info
ding info gcc
```

## Installation

Copy ding to `/usr/local/bin/`:

```bash
sudo cp v2/src/ding-v2/ding.py /usr/local/bin/ding
sudo chmod +x /usr/local/bin/ding
```

## Configuration

Configuration file: `~/.dingo/ding.conf`

```yaml
# Caching
cache:
  enabled: true
  max-size: 500M
  ttl: 86400           # 24 hours

# Repositories
repositories:
  - name: ubuntu-main
    enabled: true
  - name: ubuntu-security
    enabled: true
  - name: ubuntu-updates
    enabled: false

# Plugins
plugins:
  enabled:
    - custom-search
  disabled: []
```

## Plugin Development

Create a plugin file `~/.dingo/plugins/my-plugin.py`:

```python
class MyPlugin:
    name = "my-plugin"
    version = "1.0"
    
    def execute(self, args):
        print(f"My plugin executed with: {args}")
        return 0
    
    def help(self):
        return "My custom ding plugin"
```

Then load it:

```bash
ding plugin load my-plugin.py
ding plugin execute my-plugin search-advanced gcc --category devel
```

## Usage Examples

### Search with Cache

```bash
# First search (builds cache)
ding search python3
# [builds cache... 2-3 seconds]

# Second search (from cache)
ding search python3
# [instant from cache]
```

### Manage Repositories

```bash
# Add Ubuntu Security repo
ding repo add ubuntu-security ppa:ubuntu/security

# See all repos
ding repo list

# Check security updates
ding search --upgradable | grep security
```

### Monitor Cache

```bash
# Check cache usage
ding cache-stats
# Total: 45 MB / 500 MB

# Clear old cache
ding cache-clean

# Rebuild index
ding cache-rebuild
```

## Architecture

```
ding (CLI)
├── cache_manager.py      # Caching system
├── repo_manager.py       # Repository management
├── plugin_loader.py      # Plugin system
└── ding.py              # Main wrapper
```

## Performance

- Cache lookups: <100ms
- Repository add: <1s
- Plugin load: <500ms
- Regular apt commands: Same as v1

## Backward Compatibility

- All v1 commands work unchanged
- v1 configuration auto-migrates
- No breaking changes

## Future Enhancements (v3+)

- Advanced plugin API
- Plugin marketplace
- Automatic updates
- Machine learning for dependency prediction
- GUI package manager

---

**ding v2 makes apt simpler, faster, and more extensible!**
