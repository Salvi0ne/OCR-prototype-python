import cv2
import pytesseract
from PIL import Image
import re
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DATE_FORMATS = [
    '%d/%m/%Y',  # 21/06/2024
    '%m/%d/%Y',  # 06/21/2024
    '%Y/%m/%d',  # 2024/06/21
    '%b %d %Y',  # Jun 21 2024
    '%d %b %Y',  # 21 Jun 2024
    '%Y-%m-%d',  # 2024-06-21 (ISO format)
]

def preprocess_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Unable to read the image. The file may be corrupted or in an unsupported format.")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return thresh
    except Exception as e:
        print(f"Error in image preprocessing: {str(e)}")
        return None

def extract_text(preprocessed_image):
    try:
        return pytesseract.image_to_string(Image.fromarray(preprocessed_image))
    except Exception as e:
        print(f"Error in text extraction: {str(e)}")
        return None

def parse_date(date_string):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass

    # If no format matches, try to extract date components
    date_components = re.findall(r'\d+|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b', date_string)
    if len(date_components) == 3:
        for fmt in ['%d %m %Y', '%m %d %Y', '%Y %m %d', '%d %b %Y', '%b %d %Y']:
            try:
                return datetime.strptime(' '.join(date_components), fmt)
            except ValueError:
                pass

    raise ValueError(f"Unable to parse date: {date_string}")

def parse_total(total_string):
    total_str = re.sub(r'[^\d.]', '', total_string)
    try:
        return float(total_str)
    except ValueError:
        raise ValueError(f"Unable to convert '{total_string}' to a float.")

def parse_receipt_with_server(text):
    api_url = os.getenv("API_ENDPOINT", "http://localhost:5000")
    try:
        response = requests.post(f"{api_url}/parse_receipt", json={'text': text})
        response.raise_for_status()
        parsed_response = response.json()
        receipt_text = parsed_response.get('response', '')
        
        parsed_data = {}
        for line in receipt_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                parsed_data[key.strip()] = value.strip()
        
        if not all(key in parsed_data for key in ['Date', 'Total Amount', 'Category']):
            raise ValueError("Parsed data is missing required fields")
        
        parsed_data['Total'] = parsed_data.pop('Total Amount')
        return parsed_data
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as e:
        print(f"Invalid parsed data: {e}")
        return None

def send_to_api(api_data):
    api_url = os.getenv("API_ENDPOINT", "http://localhost:5000")
    try:
        response = requests.post(f"{api_url}/receipts", json=api_data, timeout=5)
        if response.status_code == 201:
            receipt_id = list(response.json().keys())[0]
            print(f"Receipt data sent successfully. Receipt ID: {receipt_id}")
        else:
            print(f"Failed to send receipt data: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending data to API: {str(e)}")
        print("Make sure your Flask API server (app.py) is running on the correct endpoint")

def user_confirm_data(data):
    print("\nExtracted Data:")
    for key, value in data.items():
        print(f"{key}: {value}")
    
    while True:
        confirm = input("\nIs this information correct? (yes/no): ").strip().lower()
        if confirm == 'yes' or confirm == 'y':
            return data
        elif confirm == 'no' or confirm == 'n':
            print("\nPlease enter the correct information:")
            data['Date'] = input("Date: ")
            data['Total'] = input("Total amount: ")
            data['Category'] = input("Category (Food/Lodging/Transportation/Other): ")
            return data
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def process_receipt(image_path):
    preprocessed = preprocess_image(image_path)
    if preprocessed is None:
        return None

    text = extract_text(preprocessed)
    if text is None:
        return None

    receipt_data = parse_receipt_with_server(text)
    if receipt_data is None:
        return None

    confirmed_data = user_confirm_data(receipt_data)

    try:
        date_obj = parse_date(confirmed_data.get('Date'))
        total_float = parse_total(confirmed_data.get('Total', '0'))
    except ValueError as e:
        print(f"Error: {str(e)}. Using default values.")
        date_obj = datetime.now()
        total_float = 0.0

    api_data = {
        'date': date_obj.isoformat(),
        'category': confirmed_data.get('Category', 'Other'),
        'total': total_float
    }

    send_to_api(api_data)

    return confirmed_data

# Main execution
if __name__ == "__main__":
    while True:
        image_path = input("Enter the path to the receipt image (or 'quit' to exit): ")
        if image_path.lower() == 'quit':
            break

        processed_data = process_receipt(image_path)
        if processed_data:
            print("\nProcessed Receipt Data:")
            for key, value in processed_data.items():
                print(f"{key}: {value}")
        else:
            print("Failed to process the receipt. Please try again with a different image.")