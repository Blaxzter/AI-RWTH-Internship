import os
import random
import string
import sys
import time

import dateutil.parser
import numpy as np


def get_random_string(string_length = 10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = string_length))


def get_unix_time(time_str):
    parsed_date = dateutil.parser.parse(time_str)
    return time.mktime(parsed_date.timetuple())


def dict_factory(x):
    return {k: v for (k, v) in x if v is not None}


def weiben(x, x_1, y_1, x_2, y_2):
    b = (np.log(-np.log(1 - y_2)) - np.log(-np.log(1 - y_1))) / (np.nan_to_num(np.log(x_2)) - np.nan_to_num(np.log(x_1)))
    a = x_1 * np.power(-np.log(1 - y_1), - 1 / b)

    return 1 - np.exp(-np.power(x / a, b))

def get_outlier_probabilities(test_dec, decision_values):
    current_min = np.min(test_dec)
    min_value = current_min if current_min < decision_values['smallest_score'] \
        else decision_values['smallest_score']
    current_max = np.max(test_dec)
    max_value = current_max if current_max > decision_values['biggest_score'] \
        else decision_values['biggest_score']

    distance_to_min_value = np.abs(min_value - test_dec)
    probabilities = weiben(
        distance_to_min_value,
        decision_values['dec_threshold'] + np.abs(min_value),
        0.1,
        max_value + np.abs(min_value),
        0.99
    )

    return probabilities

def suppressOutput(func):
    def wrapper(*args, **kwargs):
        with open(os.devnull, "w") as devNull:
            original = sys.stdout
            sys.stdout = devNull
            func(*args, **kwargs)
            sys.stdout = original

    return wrapper
