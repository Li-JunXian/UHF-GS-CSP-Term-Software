from fastapi import WebSocket, WebSocketDisconnect
from ..state.datastore import TelemetryStore
import asyncio, json

class WSHandler:
    def __init__(self, store: TelemetryStore):
        self.store = store
        self.clients = set()

    async def broadcaster(self):
        last = 0
        while True:
            cur = self.store.snapshot()
            if cur and id(cur[-1]) != last:
                payload = json.dumps(cur[-1])
                await asyncio.gather(*[c.send_text(payload)
                                       for c in list(self.clients)])
                last = id(cur[-1])
            await asyncio.sleep(0.2)

    async def endpoint(self, ws: WebSocket):
        await ws.accept()
        self.clients.add(ws)
        try:
            while True:
                await ws.receive_text()     # ignore; one-way
        except WebSocketDisconnect:
            self.clients.discard(ws)
