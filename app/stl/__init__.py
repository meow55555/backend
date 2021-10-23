from os import popen, system

def get_status(key=None):
    if key:
        res = popen(f"stl status {key}").read()
        return res # placeholder
    else:
        res = popen(f"stl status")
        return res # placeholder

def add_key(key):
    system(f"stl key add {key}")