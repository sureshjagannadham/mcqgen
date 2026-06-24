# ===========================
# logger.py (Project Logging Setup)
# ===========================

# Import required modules
import logging        # Built-in Python logging system
import os             # For working with file paths and directories
from datetime import datetime  # To generate timestamp for log file names

# Create a unique log file name using current date & time
# Example: 2026-06-24_17_05_30.log
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.log"

# Define the path for the logs folder inside the project directory
log_path = os.path.join(os.getcwd(), "logs")

# Ensure the logs folder exists (creates if missing)
# exist_ok=True avoids error if folder already exists
os.makedirs(log_path, exist_ok=True)

# Combine folder path + file name → full log file path
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# Configure the logging system
logging.basicConfig(
    level=logging.INFO,          # Log INFO and above (INFO, WARNING, ERROR, CRITICAL)
    filename=LOG_FILEPATH,       # Save logs into the file created above
    format="[% (asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
    # Format explanation:
    # %(asctime)s  → timestamp of log
    # %(lineno)d   → line number in code where log was triggered
    # %(name)s     → logger/module name
    # %(levelname)s→ log level (INFO, ERROR, etc.)
    # %(message)s  → actual log message
)

# ===========================
# PURPOSE OF THIS FILE:
# ---------------------------
# - Sets up a logging system for the whole project.
# - Instead of using print(), developers call logging.info(), logging.error(), etc.
# - All logs are automatically saved into timestamped files inside /logs folder.
# - Helps track program execution and debug issues easily.
# ===========================
