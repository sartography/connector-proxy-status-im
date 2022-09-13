import json

from flask import Flask, Response, request

app = Flask(__name__)

@app.before_first_request
def load_plugins():
    print('load the plugins once here?')

@app.route('/v1/commands')
def list_commands():
    def describe_command(plugin_name, command_name, command):
        parameters = PluginService.command_params_desc(command)
        plugin_display_name = PluginService.plugin_display_name(plugin_name)
        command_id = PluginService.command_id(plugin_name, command_name)
        return { 'id': command_id, 'parameters': parameters }

    commands_by_plugin = PluginService.available_commands_by_plugin()
    descriptions = []

    for plugin_name, commands in commands_by_plugin.items():
        for command_name, command in commands.items():
            description = describe_command(plugin_name, command_name, command)
            descriptions.append(description)

    return Response(json.dumps(descriptions), status=200, mimetype='application/json')

@app.route('/v1/do/<plugin_display_name>/<command_name>')
def do_command(plugin_display_name, command_name):
    command = PluginService.command_named(plugin_display_name, command_name)
    if command is None:
        return Response('Command not found', status=404)

    params = request.args.to_dict()
    result = command(**params)

    return Response(result['response'], status=result['status'], mimetype=result['mimetype'])

# TODO move out to own home
import importlib
import inspect
import pkgutil
import types
import typing

class PluginService:
    PLUGIN_PREFIX = 'connector_'

    @staticmethod
    def plugin_display_name(plugin_name):
        return plugin_name.removeprefix(PluginService.PLUGIN_PREFIX)

    @staticmethod
    def plugin_name_from_display_name(plugin_display_name):
        return PluginService.PLUGIN_PREFIX + plugin_display_name
    
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
                plugin_name: {
                    command_name: command 
                    for command_name, command 
                    in PluginService.commands_for_plugin(plugin_name, plugin) 
                } 
            for plugin_name, plugin
            in PluginService.available_plugins().items()
        }

    @staticmethod
    def command_id(plugin_name, command_name):
        plugin_display_name = PluginService.plugin_display_name(plugin_name)
        return f'{plugin_display_name}/{command_name}'

    @staticmethod
    def command_named(plugin_display_name, command_name):
        plugin_name = PluginService.plugin_name_from_display_name(plugin_display_name)
        available_commands_by_plugin = PluginService.available_commands_by_plugin()

        try:
            return available_commands_by_plugin[plugin_name][command_name]
        except:
            return None

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

    @staticmethod
    def param_annotation_desc(param):
        """Parses a callable parameter's type annotation, if any, to form a ParameterDescription."""
        param_id = param.name
        param_type_desc = "any"

        none_type = type(None)
        supported_types = {str, int, bool, none_type}
        unsupported_type_marker = object

        annotation = param.annotation

        if annotation in supported_types:
            annotation_types = {annotation}
        else:
            # an annotation can have more than one type in the case of a union
            # get_args normalizes Union[str, dict] to (str, dict)
            # get_args normalizes Optional[str] to (str, none)
            # all unsupported types are marked so (str, dict) -> (str, unsupported)
            # the absense of a type annotation results in an empty set
            annotation_types = set(
                map(
                    lambda t: t if t in supported_types else unsupported_type_marker,
                    typing.get_args(annotation),
                )
            )

        # a parameter is required if it has no default value and none is not in its type set
        param_req = param.default is param.empty and none_type not in annotation_types

        # the none type from a union is used for requiredness, but needs to be discarded
        # to single out the optional type
        annotation_types.discard(none_type)

        # if we have a single supported type use that, else any is the default
        if len(annotation_types) == 1:
            annotation_type = annotation_types.pop()
            if annotation_type in supported_types:
                param_type_desc = annotation_type.__name__

        return {"id": param_id, "type": param_type_desc, "required": param_req}

    @staticmethod
    def command_params_desc(command):
        sig = inspect.signature(command)
        params_to_skip = ['self', 'kwargs']
        sig_params = filter(
            lambda param: param.name not in params_to_skip, sig.parameters.values()
        )
        params = [
            PluginService.param_annotation_desc(param) for param in sig_params
        ]

        return params

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
