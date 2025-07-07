from fastapi import FastAPI, Depends
from ..state.datastore import TelemetryStore
store: TelemetryStore | None = None   # injected from main

def get_store() -> TelemetryStore:
    return store

api = FastAPI()

@api.get("/telemetry")
def telemetry(s: TelemetryStore = Depends(get_store)):
    return s.snapshot()
