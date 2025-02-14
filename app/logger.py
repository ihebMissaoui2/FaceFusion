import logging
import sys

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Create a logger
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.DEBUG)  # Set the logging level

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# File handler (optional, saves logs to a file)
file_handler = logging.FileHandler("app.log", mode="a")
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
