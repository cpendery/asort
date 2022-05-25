import argparse

from asort import api


def cli() -> argparse.Namespace:
    """
    run the cli

    :return: the cli's parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        metavar="path",
        type=str,
        nargs="+",
        help="sort all Python files, starting from the given path, recursively.",
    )
    return parser.parse_args()


def main():
    args = cli()
    asort = api.ASort()
    for path in args.paths:
        asort.process_path(path)
