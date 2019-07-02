"""Zeff subcommand to create a template builder for users."""
__docformat__ = "reStructuredText en"
__all__ = ["template_subparser"]

import sys
import pathlib
from string import Template


def template_subparser(subparsers):
    """Add the ``template`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the template sub-command.
    """
    import argparse

    parser = subparsers.add_parser("template")
    parser.add_argument(
        "name",
        help="Name of record to be built. Class name will be ${name}RecordBuilder.",
    )
    parser.add_argument(
        "-o",
        dest="filepath",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Path for file to save new builder class (default: stdout).",
    )
    parser.set_defaults(func=build_from_template)


def build_from_template(options):
    """Create a new builder class."""
    sys.stdout = options.filepath
    template_path = pathlib.PurePath(__file__).parent.joinpath("RecordBuilder.template")
    with open(template_path, "r") as template_file:
        template = Template(template_file.read())
    print(template.safe_substitute(name=options.name))
