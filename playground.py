from dotenv import load_dotenv
import logging
import os
from functools import wraps

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def hello_validator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not str(kwargs):
          print('?')
          return False, "No greetings provided"
        return func(*args, **kwargs)
    return wrapper

@hello_validator
def hello_world(greetings):
    print(greetings)


if __name__ == "__main__":
     # print( DATABASE_URL)
     # logging.basicConfig(level=logging.WARNING)
     hello_world(1)




