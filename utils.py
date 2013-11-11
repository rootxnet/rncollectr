from os import popen
import subprocess


def getoutput(command):
    """Return output (stdout or stderr) of executing cmd in a shell.
    This is an improved version of subprocess.getoutput() function.
    It allows running commands on MS Windows systems in addition to POSIX systems.
    """
    if subprocess.mswindows:
        cmd = '( ' + command + ' ) 2>&1'
    else:
        cmd = '{ ' + command + '; } 2>&1'
    with popen(cmd, 'r') as pipe:
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
    if sts:
        raise subprocess.CalledProcessError(sts, command, text)
    return text
