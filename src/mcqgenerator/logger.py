import logging
import os
import datetime import datetime

LOG_FILE = f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log"

log_path =os.path.join(os.getcwd(), "logs",)
os.mkdir(log_path, exist_ok=True)
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)
logging(level=logging.INFO,
    filename=LOG_FILEPATH,
    format="[% (asctime)s] % (lineno)d % (name)s - % (levelname)s - % (message)s"
)
