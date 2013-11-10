"""RNCollectr is used to gather output from defined plugins and transfer it to Graphite server.

"""
import base64
import functools
from importlib import import_module
import threading
from time import sleep
from urllib.request import Request, urlopen
import settings
from utils import getoutput
from validators import validate_plugin_definition, validate_command_definition


def send_result(value, chart):
    request = Request(settings.HG_URL, bytes("{chart} {value}".format(chart=chart, value=value), encoding="utf-8"))
    request.add_header("Authorization",
                       "Basic " + base64.b64encode(bytes(settings.API_KEY, encoding="utf-8")).decode("utf-8"))
    result = urlopen(request)
    return result.status


def handle_plugin(plugin_name, chart, **params):
    plugin = import_module("plugins.modules." + plugin_name)
    result = plugin.main(**params).strip()
    send_result(result, chart)


def handle_command(command, chart):
    result = getoutput(command).strip()
    send_result(result, chart)


def worker(func, delay):
    while True:
        func()
        sleep(delay)


if __name__ == "__main__":
    threads = []

    for plugin in settings.PLUGINS:
        validate_plugin_definition(plugin)
        func = functools.partial(handle_plugin, plugin["plugin"], plugin["chart"], **plugin["params"])
        t = threading.Thread(target=functools.partial(worker, func, plugin["delay"]))
        threads.append(t)

    for command in settings.COMMANDS:
        validate_command_definition(command)
        func = functools.partial(handle_command, command["cmd"], command["chart"])
        t = threading.Thread(target=functools.partial(worker, func, command["delay"]))
        threads.append(t)

    for _thread in threads:
        _thread.start()
