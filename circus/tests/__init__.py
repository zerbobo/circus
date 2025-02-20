import os

import papa
import zmq
from circus.util import configure_logger
from circus import logger


_CONFIGURED = False

if not _CONFIGURED and 'TESTING' in os.environ:
    configure_logger(logger, level='CRITICAL', output=os.devnull)
    _CONFIGURED = True


def setUp():
    from circus import _patch   # NOQA
    papa.set_default_port(30303)
    papa.set_default_connection_timeout(5)


def tearDown():
    # There seems to some issue with context cleanup and Python >= 3.4
    # making the tests hang at the end
    # Explicitly destroying the context seems to do the trick
    # cf https://github.com/zeromq/pyzmq/pull/513
    zmq.Context.instance().destroy()

    with papa.Papa() as p:
        p.exit_if_idle()
