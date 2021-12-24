import random
import string
import sys
import os

def get_random_string(string_length = 10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = string_length))


def dict_factory(x):
    return {k: v for (k, v) in x if v is not None}

def suppressOutput(func):
    def wrapper(*args, **kwargs):
        with open(os.devnull,"w") as devNull:
            original = sys.stdout
            sys.stdout = devNull
            func(*args, **kwargs)
            sys.stdout = original
    return wrapper