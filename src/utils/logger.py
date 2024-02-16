import os
import datetime
from src.constants.main import DEV_LOG_LEVEL

class Logger:
    def __init__(self, service_name):
        self.service_name = service_name
        self.debug_enabled = os.getenv(DEV_LOG_LEVEL, False)

    def log(self, level, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{current_time}][{self.service_name}][{level}] - {message}\n"

        print(log_message, end="")

    def info(self, message):
        self.log("INFO", message)

    def error(self, message):
        self.log("ERROR", message)

    def debug(self, message):
        if self.debug_enabled:
            self.log("DEBUG", message)
