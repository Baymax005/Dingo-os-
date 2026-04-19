"""
Cache Manager for ding v2
Handles caching of package searches and operations
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta

class CacheManager:
    """Manages package search caching with TTL"""

    def __init__(self, cache_dir=None):
        if cache_dir is None:
            self.cache_dir = Path.home() / '.dingo' / 'cache'
        else:
            self.cache_dir = Path(cache_dir)

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.cache_dir / 'index.json'
        self.max_size = 500 * 1024 * 1024  # 500MB default
        self.load_index()

    def load_index(self):
        """Load cache index from disk"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r') as f:
                    self.index = json.load(f)
            except:
                self.index = {}
        else:
            self.index = {}

    def save_index(self):
        """Save cache index to disk"""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def get(self, key):
        """Retrieve cached value if not expired"""
        if key not in self.index:
            return None

        entry = self.index[key]

        # Check if expired
        expires_at = datetime.fromisoformat(entry['expires_at'])
        if datetime.now() > expires_at:
            self._delete_entry(key)
            return None

        # Read from file
        cache_file = self.cache_dir / entry['file']
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    return f.read()
            except:
                return None

        return None

    def set(self, key, value, ttl=86400):
        """Store value in cache with TTL"""
        # Generate cache filename
        cache_filename = f"{key.replace(':', '_')}.cache"
        cache_file = self.cache_dir / cache_filename

        # Write value to file
        try:
            with open(cache_file, 'w') as f:
                f.write(value)
        except Exception as e:
            print(f"Cache write error: {e}")
            return

        # Update index
        expires_at = (datetime.now() + timedelta(seconds=ttl)).isoformat()
        self.index[key] = {
            'file': cache_filename,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at,
            'size': len(value),
            'ttl': ttl
        }

        self.save_index()

    def clear(self):
        """Clear all cache"""
        import shutil
        try:
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self.index = {}
            self.save_index()
        except Exception as e:
            print(f"Cache clear error: {e}")

    def _delete_entry(self, key):
        """Delete expired cache entry"""
        if key in self.index:
            cache_file = self.cache_dir / self.index[key]['file']
            try:
                if cache_file.exists():
                    cache_file.unlink()
            except:
                pass

            del self.index[key]
            self.save_index()

    def stats(self):
        """Return cache statistics"""
        total_size = 0
        item_count = 0

        for key, entry in self.index.items():
            total_size += entry.get('size', 0)
            item_count += 1

        # Format size
        size_mb = total_size / (1024 * 1024)
        max_mb = self.max_size / (1024 * 1024)

        last_updated = "Never"
        if self.index:
            last_update_times = [
                entry.get('created_at')
                for entry in self.index.values()
                if entry.get('created_at')
            ]
            if last_update_times:
                last_updated = max(last_update_times)

        return {
            'total_size': f"{size_mb:.1f} MB",
            'max_size': f"{max_mb:.0f} MB",
            'item_count': item_count,
            'last_updated': last_updated
        }

    def rebuild(self):
        """Rebuild cache index (remove expired entries)"""
        expired_keys = []

        for key, entry in self.index.items():
            expires_at = datetime.fromisoformat(entry['expires_at'])
            if datetime.now() > expires_at:
                expired_keys.append(key)

        # Delete expired entries
        for key in expired_keys:
            self._delete_entry(key)

        print(f"Cache rebuild: removed {len(expired_keys)} expired entries")
