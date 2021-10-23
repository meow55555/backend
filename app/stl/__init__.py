from os import popen, system


def get_status(key=None, verbose=False):
    if not verbose:
        if key:
            res = popen(f"stl status {key}").read()
            return res  # placeholder
        else:
            res = popen(f"stl status")
            return res  # placeholder
    else:
        if key:
            res = popen(f"stl status {key}").read()
            # add some db stuff
            return res  # placeholder
        else:
            res = popen(f"stl status {key}").read()
            # add some db stuff
            return res  # placeholder


def add_key(key):
    system(f"stl key add {key}")
