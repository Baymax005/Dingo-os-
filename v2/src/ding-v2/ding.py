#!/usr/bin/env python3
"""
Dingo OS v2 - Enhanced Package Manager
Main entry point for ding with caching, repo management, and plugins
"""

import sys
import os
import argparse
from pathlib import Path

# Import v2 modules
from cache_manager import CacheManager
from repo_manager import RepoManager
from plugin_loader import PluginLoader

__version__ = "2.0"
__author__ = "Dingo OS Contributors"

class DingPackageManager:
    """Enhanced package manager with caching and plugins"""

    def __init__(self):
        self.cache_dir = Path.home() / '.dingo' / 'cache'
        self.plugin_dir = Path.home() / '.dingo' / 'plugins'
        self.config_file = Path.home() / '.dingo' / 'ding.conf'

        # Initialize components
        self.cache = CacheManager(self.cache_dir)
        self.repos = RepoManager()
        self.plugins = PluginLoader(self.plugin_dir)

        # Create necessary directories
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.plugin_dir.mkdir(parents=True, exist_ok=True)

    def install(self, package):
        """Install a package"""
        print(f"Installing {package}...")
        # Check cache first
        cached = self.cache.get(f"install:{package}")
        if cached:
            print(f"[CACHED] {cached}")
            return

        # Execute apt install
        import subprocess
        result = subprocess.run(['apt', 'install', '-y', package],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ Installed: {package}")
            self.cache.set(f"install:{package}", f"Installed: {package}")
        else:
            print(f"✗ Failed to install: {package}")
            print(result.stderr)

    def remove(self, package):
        """Remove a package"""
        print(f"Removing {package}...")
        import subprocess
        result = subprocess.run(['apt', 'remove', '-y', package],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✓ Removed: {package}")
        else:
            print(f"✗ Failed to remove: {package}")

    def search(self, query):
        """Search for packages (with caching)"""
        # Check cache first
        cached = self.cache.get(f"search:{query}")
        if cached:
            print(f"[CACHED] Results for '{query}':")
            print(cached)
            return

        print(f"Searching for '{query}'...")
        import subprocess
        result = subprocess.run(['apt-cache', 'search', query],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print(result.stdout)
            # Cache the result
            self.cache.set(f"search:{query}", result.stdout, ttl=86400)
        else:
            print(f"Search failed")

    def update(self):
        """Update package lists"""
        print("Updating package lists...")
        import subprocess
        result = subprocess.run(['sudo', 'apt', 'update'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Package lists updated")
            # Clear search cache on update
            self.cache.clear()
        else:
            print("✗ Failed to update")

    def upgrade(self):
        """Upgrade installed packages"""
        print("Upgrading packages...")
        import subprocess
        result = subprocess.run(['sudo', 'apt', 'upgrade', '-y'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Packages upgraded")
        else:
            print("✗ Failed to upgrade")

    def cache_stats(self):
        """Show cache statistics"""
        stats = self.cache.stats()
        print("Cache Statistics:")
        print(f"  Total size: {stats['total_size']}")
        print(f"  Items cached: {stats['item_count']}")
        print(f"  Last updated: {stats['last_updated']}")

    def cache_clean(self):
        """Clear cache"""
        self.cache.clear()
        print("✓ Cache cleared")

    def cache_rebuild(self):
        """Rebuild cache index"""
        print("Rebuilding cache index...")
        self.cache.rebuild()
        print("✓ Cache rebuilt")

    def repo_add(self, name, url):
        """Add a repository"""
        print(f"Adding repository: {name}")
        self.repos.add_repo(name, url)
        print(f"✓ Repository added: {name}")

    def repo_list(self):
        """List repositories"""
        repos = self.repos.list_repos()
        print("Enabled Repositories:")
        for repo in repos:
            status = "✓" if repo.get('enabled') else "✗"
            print(f"  {status} {repo['name']}: {repo['url']}")

    def repo_remove(self, name):
        """Remove a repository"""
        print(f"Removing repository: {name}")
        self.repos.remove_repo(name)
        print(f"✓ Repository removed: {name}")

    def plugin_list(self):
        """List available plugins"""
        plugins = self.plugins.list_plugins()
        print("Available Plugins:")
        for plugin in plugins:
            print(f"  • {plugin['name']} (v{plugin['version']})")

    def plugin_load(self, plugin_file):
        """Load a plugin"""
        print(f"Loading plugin: {plugin_file}")
        self.plugins.load_plugin(plugin_file)
        print(f"✓ Plugin loaded: {plugin_file}")

    def help(self):
        """Show help message"""
        print("""
ding v2.0 - Enhanced Package Manager

USAGE:
    ding <command> [options]

COMMANDS:
    install PACKAGE         Install a package
    remove PACKAGE          Remove a package
    search TERM             Search for packages (cached)
    update                  Update package lists
    upgrade                 Upgrade all packages

    cache-stats             Show cache statistics
    cache-clean             Clear cache
    cache-rebuild           Rebuild cache index

    repo add NAME URL       Add repository
    repo list               List repositories
    repo remove NAME        Remove repository

    plugin list             List plugins
    plugin load FILE        Load plugin

    --help                  Show this help
    --version               Show version

EXAMPLES:
    ding install nginx
    ding search python3
    ding cache-stats
    ding repo add ubuntu-security ppa:ubuntu/security
    ding plugin load my-commands.py

For more info: man ding
        """)

def main():
    parser = argparse.ArgumentParser(
        prog='ding',
        description='Dingo OS v2 Enhanced Package Manager'
    )

    parser.add_argument('--version', action='version', version=f'ding {__version__}')
    parser.add_argument('--help', action='store_true', help='Show help')

    args, cmd_args = parser.parse_known_args()

    ding = DingPackageManager()

    if args.help or len(sys.argv) == 1:
        ding.help()
        return 0

    if len(cmd_args) == 0:
        ding.help()
        return 0

    command = cmd_args[0]

    # Route commands
    if command == 'install' and len(cmd_args) > 1:
        ding.install(cmd_args[1])
    elif command == 'remove' and len(cmd_args) > 1:
        ding.remove(cmd_args[1])
    elif command == 'search' and len(cmd_args) > 1:
        ding.search(cmd_args[1])
    elif command == 'update':
        ding.update()
    elif command == 'upgrade':
        ding.upgrade()
    elif command == 'cache-stats':
        ding.cache_stats()
    elif command == 'cache-clean':
        ding.cache_clean()
    elif command == 'cache-rebuild':
        ding.cache_rebuild()
    elif command == 'repo' and len(cmd_args) > 1:
        if cmd_args[1] == 'add' and len(cmd_args) > 3:
            ding.repo_add(cmd_args[2], cmd_args[3])
        elif cmd_args[1] == 'list':
            ding.repo_list()
        elif cmd_args[1] == 'remove' and len(cmd_args) > 2:
            ding.repo_remove(cmd_args[2])
    elif command == 'plugin' and len(cmd_args) > 1:
        if cmd_args[1] == 'list':
            ding.plugin_list()
        elif cmd_args[1] == 'load' and len(cmd_args) > 2:
            ding.plugin_load(cmd_args[2])
    else:
        print(f"Unknown command: {command}")
        ding.help()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
