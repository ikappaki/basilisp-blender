"""Functions that depend on the `bpy` module."""

import atexit
import importlib
import sys

from basilisp.lang import keyword as kw
from basilisp.lang import map as lmap
from basilisp.lang.util import munge

def server_thread_async_start(host="127.0.0.1", port=0, nrepl_port_filepath=None):
    """Start an nREPL server on the specified `host` and `port` on a
    separate thread.

    The server binds to "127.0.0.1" by default and uses a random port
    if `port` is set to 0 (the default).

    Client requests are queued rather than executed immediately. The
    function returns two callables: one for processing the queued
    requests, and another for shutting down the server.

    The port number is saved to the `nrepl_port_filepath` for nREPL
    clients to use, if provided.

    """
    assert '"' not in host
    assert port >= 0

    nrepl_server_mod = importlib.import_module(munge("basilisp-nrepl-async.nrepl-server"))
    ret = nrepl_server_mod.server_start__BANG__(
        lmap.map(
            {
                kw.keyword("async?"): True,
                kw.keyword("host"): host,
                kw.keyword("port"): port,
                kw.keyword("nrepl-port-file"): nrepl_port_filepath,
            }
        )
    )

    assert ret is not None, ":server-error :could-not-be-started"
    work_fn = ret.get(kw.keyword("work-fn"))
    shutdown_fn = ret.get(kw.keyword("shutdown-fn"))
    assert work_fn and shutdown_fn, ":server-error :could-not-be-started"

    return work_fn, shutdown_fn


try:
    import bpy

    def server_start(
        host="127.0.0.1", port=0, nrepl_port_filepath=".nrepl-port", interval_sec=0.1
    ):
        """Start an nREPL server on a separate thread using the
        specified `host` and `port`. The server binds to "127.0.0.1"
        by default and uses a random port if `port` is set to 0 (the
        default). Client requests are queued and executed at intervals
        defined by `interval_sec` (defaulting to 0.1 seconds) using a
        `bpy.app.timers` timer for thread safety. The server is also
        registered to shut down upon program exit.

        The port number is saved to a file for nREPL clients to use. By
        default, this is an `.nrepl-port` file in the current working
        directory. If `nrepl_port_filepath` is provided, the port number is
        written to the specified filepath instead.

        """

        def work_do_safe(workfn, interval_sec):
            """Execute `workfn` return, `interval_sec` to indicate when to
            call this function again, and catch exceptions to report errors to
            stderr.

            """
            try:
                workfn()
            except Exception as e:
                print(f":nrepl-work-fn-error {e}", file=sys.stderr)
            return interval_sec

        def shutdown_safe(shutdownfn):
            """Execute `shutdownfn` and handle any exceptions by reporting
            errors to stderr.

            """
            try:
                shutdownfn()
            except Exception as e:
                print(f":nrepl-shutdown-error {e}", file=sys.stderr)

        workfn, shutdownfn = server_thread_async_start(
            host=host, port=port, nrepl_port_filepath=nrepl_port_filepath
        )

        atexit.register(lambda: shutdown_safe(shutdownfn))

        bpy.app.timers.register(lambda: work_do_safe(workfn, interval_sec))

        return shutdownfn

except ImportError:
    pass
