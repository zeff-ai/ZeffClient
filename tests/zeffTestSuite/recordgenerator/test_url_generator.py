"""Zeff test suite."""

import os
import pathlib
import urllib.parse
import pytest

from zeff.recordgenerator import (
    entry_url_generator,
    file_url_generator,
    directory_url_generator,
)


def test_invalid_dirurl():
    with pytest.raises(ValueError) as e_info:
        g = entry_url_generator("gopher://example.com/spam")
        next(g)


def test_entries():
    path = pathlib.Path.cwd()
    url = urllib.parse.urlunsplit(("file", str(path.resolve()), "", "", ""))

    def validate(sutpath):
        entries = [p.name for p in path.iterdir() if not p.name.startswith(".")]

        for entry in (os.path.basename(p) for p in entry_url_generator(sutpath)):
            assert entry in entries
            entries.remove(entry)
        assert len(entries) == 0

    validate(path)
    validate(url)


def test_file_entries():
    path = pathlib.Path.cwd()
    entries = [p for p in path.iterdir() if p.is_file()]
    entries = [p.name for p in entries if not p.name.startswith(".")]

    url = urllib.parse.urlunsplit(("file", str(path.resolve()), "", "", ""))
    for entry in (os.path.basename(p) for p in file_url_generator(url)):
        assert entry in entries
        entries.remove(entry)
    assert len(entries) == 0


def test_dir_entries():
    path = pathlib.Path.cwd()
    entries = [p for p in path.iterdir() if p.is_dir()]
    entries = [p.name for p in entries if not p.name.startswith(".")]

    url = urllib.parse.urlunsplit(("file", str(path.resolve()), "", "", ""))
    for entry in (os.path.basename(p) for p in directory_url_generator(url)):
        assert entry in entries
        entries.remove(entry)
    assert len(entries) == 0
