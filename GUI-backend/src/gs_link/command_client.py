import socket, threading, logging, time, struct
from .packet_utils import kiss_frame
from ..config import GS_IP, GS_CMD_PORT
RECONNECT = 5   # seconds

class CommandClient(threading.Thread):
    """Maintains a persistent socket to GS:1028 and offers .send_csp(bytes)."""
    def __init__(self):
        super().__init__(daemon=True)
        self.sock = None
        self.log  = logging.getLogger("CMD-Client")
        self._lock = threading.Lock()
        self.pending = []         # simple FIFO; could use Queue
        self.start()

    def run(self):
        while True:
            try:
                self.sock = socket.socket()
                self.sock.connect((GS_IP, GS_CMD_PORT))
                self.log.info(f"connected to GS cmd port {GS_IP}:{GS_CMD_PORT}")
                while True:
                    if self.pending:
                        with self._lock:
                            p = self.pending.pop(0)
                        self.sock.sendall(p)
                    else:
                        time.sleep(0.05)
            except OSError as e:
                self.log.warning(f"cmd socket error: {e}")
            time.sleep(RECONNECT)

    def send_csp(self, raw_packet: bytes):
        with self._lock:
            self.pending.append(raw_packet)
