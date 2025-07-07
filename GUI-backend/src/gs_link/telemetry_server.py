import socket, threading, logging, time, struct, pathlib
from .packet_utils import unpack_csp_header
from ..state.datastore import TelemetryStore
from ..config import LOCAL_TM_PORT, DATA_DIR

CHUNK = 4096

class TelemetryServer(threading.Thread):
    def __init__(self, store: TelemetryStore):
        super().__init__(daemon=True)
        self.store = store
        self.log = logging.getLogger("TM-Server")

    def run(self):
        srv = socket.socket()
        srv.bind(("0.0.0.0", LOCAL_TM_PORT))
        srv.listen(1)
        self.log.info(f"listening for GS downlink on :{LOCAL_TM_PORT}")
        while True:
            conn, addr = srv.accept()
            self.log.info(f"GS connected for telemetry from {addr}")
            try:
                self.handle_conn(conn)
            finally:
                conn.close()

    def handle_conn(self, conn: socket.socket):
        while True:
            # first, read header
            hdr = conn.recv(6)
            if not hdr:
                self.log.warning("GS closed telemetry socket")
                break
            h = unpack_csp_header(hdr)
            payload = b''
            remaining = h["length"]
            while remaining:
                chunk = conn.recv(remaining)
                if not chunk:
                    raise ConnectionError("socket closed mid-payload")
                payload += chunk
                remaining -= len(chunk)

            packet = {**h, "payload": payload.hex()}
            self.store.push(packet)

            # for archival
            fname = (DATA_DIR /
                     f"{time.strftime('%Y%m%dT%H%M%S')}_{h['dst']:02d}.bin")
            with open(fname, 'wb') as f:
                f.write(hdr + payload)
