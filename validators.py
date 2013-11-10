from schema import Schema, And, Optional, SchemaError

ERRORS_CHART = "Variable \"chart\" must contain name of Graphite chart."
ERRORS_DELAY = "Variable \"delay\" must be supplied. This variable defines time (s) between subsequent executions of given command/plugin."


def validate_plugin_definition(definition):
    """
    Performs plugin definition validation.
    If any errors are encountered, the help message is displayed and exit() issued.
    """
    schema = Schema({
        "plugin": And(str),
        Optional("params"): dict,
        "chart": And(str, error=ERRORS_CHART),
        "delay": And(int, error=ERRORS_DELAY)
    })
    try:
        schema.validate(definition)
    except SchemaError as e:
        error_text = "There is a problem with configuration of '{plugin}' plugin:".format(plugin=definition["plugin"])
        example_text = '\nProper syntax is (example):\n{"plugin": "forex", "params": {"currency": "EURUSD"}, "chart": "foo", "delay": 60},'
        print("\n".join([error_text, str(e), example_text]))
        exit()
    return schema


def validate_command_definition(definition):
    """
    Performs command definition validation.
    If any errors are encountered, the help message is displayed and exit() issued.
    """
    schema = Schema({
        "cmd": And(str),
        "chart": And(str, error=ERRORS_CHART),
        "delay": And(int, error=ERRORS_DELAY)
    })
    try:
        schema.validate(definition)
    except SchemaError as e:
        error_text = "There is a problem with configuration of '{plugin}' command:".format(plugin=definition["cmd"])
        example_text = '\nProper syntax is (example):\n' + \
                       r'{"cmd": r"python plugins\standalone_scripts\rand\rand.py --min-number=20 --max-number=80", "chart": "foo2", "delay": 60},'
        print("\n".join([error_text, str(e), example_text]))
        exit()
    return schema
