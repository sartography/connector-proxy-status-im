import json

from flask import Flask, Response

app = Flask(__name__)

@app.before_first_request
def load_plugins():
    print('load the plugins once here?')

@app.route('/v1/commands')
def list_commands():
    def describe_command(plugin_name, command_name, command):
        parameters = []
        plugin_display_name = PluginService.plugin_display_name(plugin_name)
        return { 'id': f'{plugin_display_name}/{command_name}', 'parameters': parameters }

    commands_by_plugin = PluginService.available_commands_by_plugin()
    descriptions = []

    for plugin_name, commands in commands_by_plugin.items():
        for command_name, command in commands:
            description = describe_command(plugin_name, command_name, command)
            descriptions.append(description)

    return Response(json.dumps(descriptions), status=200, mimetype='application/json')

# TODO move out to own file
import importlib
import inspect
import pkgutil
import types

class PluginService:
    PLUGIN_PREFIX = 'cmd_proxy_'

    @staticmethod
    def plugin_display_name(plugin_name):
        return plugin_name.removeprefix(PluginService.PLUGIN_PREFIX)
    
    @staticmethod
    def available_plugins():
        return {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules()
            if name.startswith(PluginService.PLUGIN_PREFIX)
        }

    @staticmethod
    def available_commands_by_plugin():
        return {
            name: list(PluginService.commands_for_plugin(name, plugin)) 
            for name, plugin
            in PluginService.available_plugins().items()
        }

    @staticmethod
    def modules_for_plugin(plugin):
        for finder, name, ispkg in pkgutil.iter_modules(plugin.__path__):
            if ispkg and name.startswith(PluginService.PLUGIN_PREFIX):
                sub_pkg = finder.find_module(name).load_module(name)
                yield from PluginService.modules_for_plugin(sub_pkg)
            else:
                spec = finder.find_spec(name)
                if spec is not None and spec.loader is not None:
                    module = types.ModuleType(spec.name)
                    spec.loader.exec_module(module)
                    yield name, module

    @staticmethod
    def commands_for_plugin(plugin_name, plugin):
        for module_name, module in PluginService.modules_for_plugin(plugin):
            for member_name, member in inspect.getmembers(module, inspect.isfunction):
                if member.__module__ == module_name:
                    yield member_name, member

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
