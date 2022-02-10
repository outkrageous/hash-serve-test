import string
import random
from concurrent.futures import ThreadPoolExecutor


def run_api_calls_in_threads(work_function, work_list):
    """
    Run multiple commands in multiple threads
    :param work_function: Function to execute
    :param work_list: Params for function to execute
    """
    with ThreadPoolExecutor(max_workers=40) as executor:
        for work in work_list:
            executor.submit(work_function, work)


def generate_random_string_of_length(length_of_str):
    """
    Generate a random string of specified length
    :param length_of_str: number of chars in string
    :return: str
    """
    return ''.join(random.choices(string.ascii_uppercase +
                                  string.digits, k=length_of_str))

