"""
Repository Manager for ding v2
Handles adding, removing, and managing apt repositories (PPAs)
"""

import subprocess
import re
from pathlib import Path

class RepoManager:
    """Manages apt repositories and PPAs"""

    def __init__(self, sources_file='/etc/apt/sources.list'):
        self.sources_file = sources_file
        self.sources_dir = '/etc/apt/sources.list.d/'

    def add_repo(self, name, url):
        """Add a repository (PPA support)"""
        if url.startswith('ppa:'):
            # Handle PPA format
            return self._add_ppa(name, url)
        else:
            # Handle custom repository
            return self._add_custom_repo(name, url)

    def _add_ppa(self, name, ppa_url):
        """Add PPA repository"""
        try:
            # Use add-apt-repository command
            cmd = f"sudo add-apt-repository -y {ppa_url}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"Added PPA: {name}")
                return True
            else:
                print(f"Failed to add PPA: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error adding PPA: {e}")
            return False

    def _add_custom_repo(self, name, url):
        """Add custom repository"""
        # TODO: Implement custom repo addition
        print(f"Custom repositories not yet implemented: {name}")
        return False

    def remove_repo(self, name):
        """Remove a repository"""
        try:
            cmd = f"sudo add-apt-repository -y --remove ppa:{name}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"Removed repository: {name}")
                return True
            else:
                print(f"Failed to remove repository: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error removing repository: {e}")
            return False

    def list_repos(self):
        """List all repositories"""
        repos = []

        try:
            # Read sources.list
            if Path(self.sources_file).exists():
                with open(self.sources_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            repos.append({
                                'name': self._parse_repo_name(line),
                                'url': line,
                                'enabled': True,
                                'type': 'builtin'
                            })

            # Read sources.list.d/
            sources_d = Path(self.sources_dir)
            if sources_d.exists():
                for ppa_file in sources_d.glob('*.list'):
                    with open(ppa_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                repos.append({
                                    'name': ppa_file.stem,
                                    'url': line,
                                    'enabled': True,
                                    'type': 'ppa'
                                })

        except Exception as e:
            print(f"Error reading repositories: {e}")

        return repos

    def enable_repo(self, name):
        """Enable a repository"""
        # TODO: Implement repository enabling
        print(f"Enable repository not yet implemented: {name}")
        return False

    def disable_repo(self, name):
        """Disable a repository"""
        # TODO: Implement repository disabling
        print(f"Disable repository not yet implemented: {name}")
        return False

    def _parse_repo_name(self, line):
        """Parse repository name from sources line"""
        parts = line.split()
        if len(parts) >= 4:
            return ' '.join(parts[1:3])
        return line
