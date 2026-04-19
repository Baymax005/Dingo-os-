"""
Plugin Loader for ding v2
Handles loading and executing custom plugins
"""

import importlib.util
from pathlib import Path
import sys

class PluginLoader:
    """Loads and manages ding plugins"""

    def __init__(self, plugin_dir=None):
        if plugin_dir is None:
            self.plugin_dir = Path.home() / '.dingo' / 'plugins'
        else:
            self.plugin_dir = Path(plugin_dir)

        self.plugin_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_plugins = {}

    def load_plugin(self, plugin_file):
        """Load a plugin from file"""
        plugin_path = Path(plugin_file)

        if not plugin_path.exists():
            print(f"Plugin file not found: {plugin_file}")
            return False

        try:
            # Load module
            spec = importlib.util.spec_from_file_location(
                plugin_path.stem, plugin_path
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_path.stem] = module
            spec.loader.exec_module(module)

            # Get plugin class
            if hasattr(module, 'DingPlugin'):
                plugin = module.DingPlugin()
                self.loaded_plugins[plugin.name] = plugin
                print(f"Loaded plugin: {plugin.name} v{plugin.version}")
                return True
            else:
                print(f"Plugin does not have DingPlugin class: {plugin_file}")
                return False

        except Exception as e:
            print(f"Error loading plugin: {e}")
            return False

    def list_plugins(self):
        """List all available plugins"""
        plugins = []

        # Scan plugin directory
        if self.plugin_dir.exists():
            for plugin_file in self.plugin_dir.glob('*.py'):
                if plugin_file.stem != '__init__':
                    try:
                        spec = importlib.util.spec_from_file_location(
                            plugin_file.stem, plugin_file
                        )
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        if hasattr(module, 'DingPlugin'):
                            plugin = module.DingPlugin()
                            plugins.append({
                                'name': plugin.name,
                                'version': plugin.version,
                                'description': getattr(plugin, 'description', 'No description'),
                                'file': plugin_file.name
                            })
                    except Exception as e:
                        print(f"Error scanning plugin {plugin_file.stem}: {e}")

        # Add loaded plugins
        for name, plugin in self.loaded_plugins.items():
            plugins.append({
                'name': name,
                'version': plugin.version,
                'description': getattr(plugin, 'description', 'No description'),
                'file': 'loaded'
            })

        return plugins

    def execute_plugin(self, plugin_name, command, args=None):
        """Execute a plugin command"""
        if plugin_name not in self.loaded_plugins:
            print(f"Plugin not loaded: {plugin_name}")
            return False

        plugin = self.loaded_plugins[plugin_name]

        try:
            if hasattr(plugin, 'execute'):
                result = plugin.execute(command, args or [])
                return result
            else:
                print(f"Plugin {plugin_name} does not have execute method")
                return False
        except Exception as e:
            print(f"Error executing plugin: {e}")
            return False

    def get_plugin_help(self, plugin_name):
        """Get help text from plugin"""
        if plugin_name not in self.loaded_plugins:
            return None

        plugin = self.loaded_plugins[plugin_name]

        if hasattr(plugin, 'help'):
            return plugin.help()

        return None
