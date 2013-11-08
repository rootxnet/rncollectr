import base64
import functools
from importlib import import_module
import os
import subprocess
import threading
from time import sleep
from urllib.request import Request, urlopen
import settings


def getoutput(command):
    """Return output (stdout or stderr) of executing cmd in a shell.
    This is an improved version of subprocess.getoutput() function.
    It allows running commands on MS Windows systems in addition to POSIX systems.
    """
    if subprocess.mswindows:
        cmd = '( ' + command + ' ) 2>&1'
    else:
        cmd = '{ ' + command + '; } 2>&1'
    with os.popen(cmd, 'r') as pipe:
        try:
            text = pipe.read()
            sts = pipe.close()
        except:
            process = pipe._proc
            process.kill()
            process.wait()
            raise
    if text[-1:] == '\n':
        text = text[:-1]
    return text


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

    for plugin_name, plugin_params in settings.PLUGINS.items():
        func = functools.partial(handle_plugin, plugin_name, plugin_params["chart"], **plugin_params["params"])
        t = threading.Thread(target=functools.partial(worker, func, plugin_params["delay"]))
        threads.append(t)

    for command in settings.COMMANDS:
        func = functools.partial(handle_command, command["cmd"], command["chart"])
        t = threading.Thread(target=functools.partial(worker, func, command["delay"]))
        threads.append(t)

    for _thread in threads:
        _thread.start()