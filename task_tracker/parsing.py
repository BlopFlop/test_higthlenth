import argparse
from argparse import ArgumentParser, RawTextHelpFormatter


choises = {"get": "get", "post": "post", "patch": "patch", "delete": "delete"}


def parser() -> None:

    parser_obj = ArgumentParser(
        description="Консольная программа для манипулирования задачами.",
        formatter_class=RawTextHelpFormatter,
    )
    parser_obj.add_argument(
        "Tasks",
    )
