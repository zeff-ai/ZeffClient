"""Zeff collection of URL Generators."""
import pathlib
import urllib

__all__ = ["entry_url_generator", "file_url_generator", "directory_url_generator"]

# To Do Generators
# 1. HTTP index URL generator


def entry_url_generator(dirurl, allow=lambda p: True):
    """URL generator of entries in a path.

    Given a directory this will generate a URL to each entry in the
    directory.

    :param dirurl: The URL to the directory. This may be an explicit or
        implicit ``file`` URL.

    :param allow: A filter that accepts a ``pathlib.Path`` and returns
        ``True`` if it is acceptable: i.e. if only files are wanted then
        the using ``lambda p: p.is_file()`` would filter out any non-files.
    """
    dirurl = str(dirurl)
    url_parts = urllib.parse.urlsplit(dirurl)
    if url_parts.scheme in ["", "file"]:
        dirpath = pathlib.Path(url_parts.path)
    else:
        raise ValueError("URL is not a ``file`` scheme.")
    for path in (p for p in dirpath.iterdir() if allow(p)):
        if path.name.startswith("."):
            continue
        url = urllib.parse.urlunsplit(("file", "", str(path), "", ""))
        yield url


def file_url_generator(dirurl):
    """URL generator of files in a path.

    Given a directory this will generate a URL to each file in the
    directory.

    :param dirurl: The URL to the directory. This may be an explicit or
        implicit ``file`` URL.
    """
    for entry in entry_url_generator(dirurl, allow=lambda p: p.is_file()):
        yield entry


def directory_url_generator(dirurl):
    """URL generator of directories in a path.

    Each directory in the ``dirpath`` will be generated as a file
    scheme URL.

    :param dirurl: The URL to the directory. This may be an explicit or
        implicit ``file`` URL.
    """
    for entry in entry_url_generator(dirurl, allow=lambda p: p.is_dir()):
        yield entry
