import socket, threading, struct, time, logging
from config import GS_TM_PORT
from utils.csp import unpack_header   # you’ll add utils later

class TelemetryServer:
    def __init__(self, store, host='0.0.0.0', port=GS_TM_PORT):
        self.store, self.host, self.port = store, host, port
        self.log = logging.getLogger('TM-Server')

    def start(self):
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def _run(self):
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen(1)
        self.log.info(f'Telemetry server listening @ {self.port}')
        conn, addr = s.accept()
        self.log.info(f'GS connected from {addr}')
        while True:
            header = conn.recv(6)
            if not header:
                break
            pri, src, dst, dport, sport, length = unpack_header(header)
            payload = conn.recv(length)
            pkt = {
                "timestamp": time.time(),
                "src": src, "dst": dst,
                "src_port": sport, "dst_port": dport,
                "payload": payload.hex()
            }
            self.store.push(pkt)
            self.log.debug(f'Pkt {pkt}')
