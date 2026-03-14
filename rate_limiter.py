import time
import os

class RateLimiter:
    def __init__(self):
        self.interval = 60 / int(os.getenv("EMAILS_PER_MINUTE"))
        self.last_sent = 0

    def wait(self):
        now = time.time()
        elapsed = now - self.last_sent

        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)

        self.last_sent = time.time()
