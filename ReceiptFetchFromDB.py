from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Receipt
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECURITY_KEY = os.getenv("SECURITY_KEY", "123456789qwertyuiop")

def fetch_receipts():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        receipts = session.query(Receipt).all()

        print("Fetched Receipts:")
        print("=" * 30)
        for receipt in receipts:
            print(f"receipt id: {receipt.id}")
            print(f"date: {receipt.date.strftime('%Y-%m-%d')}")
            print(f"total: {receipt.total:.2f}")
            print(f"category: {receipt.category}")
            print("=" * 30)

        return receipts
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    fetch_receipts()
