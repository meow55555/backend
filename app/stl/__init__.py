from os import system


def add_key(key):
    system(f"stl key add {key}")


def del_connection(hash_key):
    system(f"stl disconnect {hash_key}")
