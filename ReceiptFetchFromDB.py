# fetch_receipts.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Receipt  # Import the Receipt model from your app
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

def fetch_receipts():
    # Create an engine and session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Query all receipts
        receipts = session.query(Receipt).all()

        # Print receipts in the specified format
        print("Fetched Receipts:")
        print("=" * 30)
        for receipt in receipts:
            print(f"receipt id: {receipt.id}")
            print(f"date: {receipt.date.strftime('%Y-%m-%d')}")  # Format date as YYYY-MM-DD
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