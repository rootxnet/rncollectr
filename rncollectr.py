"""RNCollectr is used to gather output from defined plugins and transfer it to Graphite server.

"""
import base64
import functools
from importlib import import_module
from subprocess import CalledProcessError
import threading
from time import sleep
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
import settings
from utils import getoutput
from validators import validate_plugin_definition, validate_command_definition


def send_result(value, chart):
    """
    Sends data contained in ``value`` to ``chart`` using HostedGraphite's HTTP API which lives under HG_URL.
    Relevant error messages are displayed if there are any problems while communicating with API.

    Returns status code, 202 if everything goes right.

    """
    request = Request(settings.HG_URL, bytes("{chart} {value}".format(chart=chart, value=value), encoding="utf-8"))
    request.add_header("Authorization",
                       "Basic " + base64.b64encode(bytes(settings.API_KEY, encoding="utf-8")).decode("utf-8"))
    try:
        result = urlopen(request)
    except HTTPError as e:
        if e.code in [401, 403]:
            print("Forbidden: your API key was denied.")
        if e.code == 404:
            print("Not found: the HG_URL you provided is not valid URL.")
        return False
    except URLError as e:
        print(e)
        return False
    return result.status


def handle_plugin(plugin_name, chart, **params):
    """
    Dynamically imports ``plugin_name`` from `plugin.modules`, executes it using ``**params``
    then sends the collected result to given ``chart``.

    """
    plugin = import_module("plugins.modules." + plugin_name)
    result = plugin.main(**params).strip()
    send_result(result, chart)


def handle_command(command, chart):
    """
    Fires off ``command`` and sends the collected result to given ``chart``.

    """
    result = getoutput(command).strip()
    send_result(result, chart)


def worker(func, delay):
    """
    Wrapper which is used to convert passed callable ``func`` into daemon which periodically
    fires off given callable.

    Any errors / exceptions coming from passed callable stops the daemon.

    """
    while True:
        try:
            func()
        except ImportError as e:
            print("There is a problem with your plugin configuration: {0}".format(e))
            break
        except (CalledProcessError, Exception) as e:
            print(e)
            break
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
