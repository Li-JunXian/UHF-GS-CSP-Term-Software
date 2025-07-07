from pathlib import Path
import os

GS_IP          = os.getenv("GS_IP",  "127.0.0.1")   # where the C GS runs
GS_CMD_PORT    = int(os.getenv("GS_CMD_PORT", 1028))
LOCAL_TM_PORT  = int(os.getenv("LOCAL_TM_PORT", 1025))
API_PORT       = int(os.getenv("API_PORT", 8000))

# file cache for saving raw .bin if you want
DATA_DIR       = Path(os.getenv("DATA_DIR", "./data")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_LEVEL      = os.getenv("LOG_LEVEL", "INFO")
