# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))


# -- Project information -----------------------------------------------------

project = "ZeffClient"
copyright = "2019, Ziff, Inc."
author = "Lance Finn Helsten <lanhel@flyingtitans.com>"

# The full version, including alpha/beta/rc tags
from pkg_resources import get_distribution

release = get_distribution("ZeffClient").version

version = ".".join(release.split(".")[:2])


# -- General configuration ---------------------------------------------------

exclude_patterns = []

extensions = ["sphinx.ext.autodoc", "sphinxcontrib.plantuml"]

templates_path = ["_templates"]

today_fmt = "%d %B %Y"


# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"

html_static_path = ["_static"]
