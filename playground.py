from dotenv import load_dotenv
import logging
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if __name__ == "__main__":
     print(SECURITY_KEY, DATABASE_URL)
     logging.basicConfig(level=logging.WARNING)