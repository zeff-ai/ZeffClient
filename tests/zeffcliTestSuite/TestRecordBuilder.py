import logging
logging = logging.getLogger('zeffclient.record_builder')


class TestRecordBuilder():
    """Zeff record builder callable object that builds Test records."""

    def __init__(self, *args, **argv):
        logging.debug("Create TestRecordBuilder")

    def __call__(self, url):
        logging.info("Begin building ``Test`` record from %s", url)
        return url
        logging.info("End building ``Test`` record from %s", url)

