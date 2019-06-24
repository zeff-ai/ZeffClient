"""Zeff test suite."""

from zeff.recordgenerator import generate


class mock_record():
    def __init__(self, url):
        self.url = url


def mock_builder(url):
    return mock_record(url)


def test_generate():
    urls = [
            'file://a/b/c',
            'http://example.com/x/y?spam=eggs',
            'gopher://example.com/rabbit/elmer'
        ]
    for record in generate(urls, mock_builder):
        assert record.url in urls

