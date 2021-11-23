import random
import string


def get_random_string(string_length = 10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = string_length))


def dict_factory(x):
    return {k: v for (k, v) in x if v is not None}
