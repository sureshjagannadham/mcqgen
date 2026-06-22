import logging
import os
from datetime import datetime

# 1. Fixed inner quotes and swapped colons for underscores for Windows compatibility
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.log"

# 2. Created the logs directory path cleanly
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)  # Using makedirs is safer for nested folders

LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# 3. Removed spaces inside the format placeholders
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)