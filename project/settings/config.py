import os

DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
