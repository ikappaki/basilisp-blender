import os
import threading

import nrepl as nrepl_client
import pytest

import tests.basilisp_blender.integration.test_utils as tu

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.getenv("RUNNER_OS", "Linux") != "Linux",
    reason="GHA UI testing is only supported on Linux.",
)
def test_server_start(tmp_path):
    codefile = tmp_path / "server-start-code-file.py"
    portfile = tmp_path / ".basilisp-blender-int-test-port"
    logfile = tmp_path / "basilisp-blender-int-server-start.log"
    print(f":logging-to {logfile}")
    with open(codefile, "w") as file:
        file.write(
            f"""from basilisp_blender import nrepl, log_level_set
import logging
import sys
print(":start")
sys.stdout.flush()
log_level_set(logging.DEBUG, {repr(str(logfile))})
logging.debug(":begin")
shutdownfn = nrepl.server_start(nrepl_port_filepath={repr(str(portfile))})
logging.debug(":end")
"""
        )

    process = None
    try:
        process = tu.blender_eval_file(codefile)
        tu.file_exists_wait(portfile, 10, 0.5)
        assert os.path.exists(str(portfile))

        port = None
        with open(portfile, "r") as file:
            content = file.read().strip()
            port = int(content)

        assert isinstance(port, int) and port > 0

        print(f":port {port}")

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
        client_thread.join(timeout=20)
        assert not client_thread.is_alive()
        process.terminate()
        out, error = process.communicate()
        assert "nREPL server started on port" in out
    finally:
        if process:
            process.terminate()
            out, error = process.communicate()
            print(f"::process :error {error}")
            print(f"::process :out {out}")
            if os.path.exists(str(logfile)):
                with open(logfile, "r") as file:
                    print(f":lpy-log-contents {file.read()}")
