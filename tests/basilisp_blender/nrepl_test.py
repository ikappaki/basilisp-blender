import threading
import time

import nrepl as nrepl_client

from basilisp_blender.nrepl import server_thread_async_start


def work_thread_do(workfn, interval_sec=0.1):
    """Creates and starts a daemon thread that calls the `workfn`
    repeatedly in a loop pausing for `internal_secs` seconds (defaults
    to 0.1) between executions.

    Returns the thread object and a `threading.Event`. When this event
    is set, the loop will terminate and the thread will exit.

    """
    stop_event = threading.Event()

    def work_do():
        try:
            while not stop_event.wait(interval_sec):
                workfn()
                time.sleep(interval_sec)
        except e:
            print(f":work-thread-error {e}")

    thread = threading.Thread(target=work_do, daemon=True)
    thread.start()
    return thread, stop_event


def test_server_thread_async_start(tmpdir):
    portfile = tmpdir / ".basilisp-blender-test-port"
    shutdownfn = None
    work_thread = None
    work_stop_event = None
    try:
        workfn, shutdownfn = server_thread_async_start(
            nrepl_port_filepath=str(portfile)
        )

        assert workfn and shutdownfn, ":server-error :could-not-start"

        port = None
        with open(portfile, "r") as file:
            content = file.read().strip()
            port = int(content)

        assert isinstance(port, int) and port > 0

        work_thread, work_stop_event = work_thread_do(workfn)

        def nrepl_client_test():
            client = None
            try:
                client = nrepl_client.connect(f"nrepl://localhost:{port}")
                client.write({"id": 1, "op": "clone"})
                result = client.read()
                assert "status" in result and result["status"] == ["done"]
                client.write({"id": 2, "op": "eval", "code": "(reduce + (range 20))"})
                result = client.read()
                assert "value" in result and result["value"] == "190"
            except Exception as e:
                assert e is None
            finally:
                if client:
                    client.close()

        client_thread = threading.Thread(target=nrepl_client_test, daemon=True)
        client_thread.start()
        client_thread.join(timeout=5)
        assert not client_thread.is_alive()

        work_stop_event.set()
        work_thread.join(timeout=5)
        assert not work_thread.is_alive()
    finally:
        if shutdownfn:
            shutdownfn()

        if work_stop_event:
            work_stop_event.set()
