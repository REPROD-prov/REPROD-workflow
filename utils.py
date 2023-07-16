import json

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def load_format_config(config_filename):
    with open(config_filename) as f:
        config = json.load(f)
        variables = config["variables"]
        del config["variables"]
        config={k:v.format(**variables) for (k,v) in config.items() if type(v)==str }
        config.update(variables)

    return dotdict(config)
