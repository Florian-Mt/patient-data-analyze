"""
Check that the provided path is an existing directory or try to create it
"""

import argparse
import os


def dir_path(path: str):
    """
    Check that the provided path is an existing directory or try to create it
    The full path is created, and an error is raised if this is not possible
    :param path: expected directory path
    :return: provided path
    """

    if os.path.isdir(path):
        return path

    try:
        os.makedirs(path)
        return path

    except OSError as error:
        raise argparse.ArgumentTypeError(f"{path} does not exist and could not be created") from error
