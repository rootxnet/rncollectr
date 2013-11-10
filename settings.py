HG_URL = "https://hostedgraphite.com/api/v1/sink"

# Hostedgraphite API key.
API_KEY = ""

# Periodically execute plugins contained in plugins/modules directory.
# Example:
#   {"plugin": "forex", "params": {"currency": "EURUSD"}, "chart": "foo", "delay": 20},
PLUGINS = (
    # Put plugins definitions here.
)

# Periodically execute shell commands, working directory is set as directory which contains this file.
# Example:
#   {"cmd": r"python plugins\standalone_scripts\rand\rand.py --min-number=20 --max-number=80", "chart": "foo2", "delay": 20},
COMMANDS = (
    # Put command definitions here.
)