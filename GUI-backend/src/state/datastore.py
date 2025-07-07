import threading, time, collections

class TelemetryStore:
    def __init__(self):
        self._lock = threading.RLock()
        self.latest = collections.deque(maxlen=1000)   # simple ring buffer

    def push(self, packet: dict):
        with self._lock:
            packet["recv_ts"] = time.time()
            self.latest.append(packet)

    def snapshot(self):
        with self._lock:
            return list(self.latest)
