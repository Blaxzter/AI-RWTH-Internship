import string
import random


def get_random_string(string_length = 10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = string_length))