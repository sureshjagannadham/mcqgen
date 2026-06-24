# ===========================
# test.py (Quick Logging Test)
# ===========================

# Import the logging system we set up in logger.py
from src.mcqgenerator.logger import logging

# Write a simple INFO level log message
logging.info("This is an info message")

# ===========================
# PURPOSE OF THIS FILE:
# ---------------------------
# - This file is just a quick test to check if your logging system works.
# - When you run: python test.py
#   → It should create a log file inside the /logs folder.
#   → That log file will contain a line like:
#       [2026-06-24 17:17:00] 2 root - INFO - This is an info message
# - Confirms that logger.py is correctly saving messages into timestamped log files.
# - Helps you verify logging setup before using it in bigger files like MCQGenerator.py or StreamlitAPP.py.
# ===========================
