import argparse
import os


def dir_path(path: str):
    if os.path.isdir(path):
        return path

    else:
        try:
            os.makedirs(path)
            return path

        except OSError:
            raise argparse.ArgumentTypeError(f"{path} cannot be created, it is not a valid directory path")
