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

# Modified function to use the Flask server for parsing
def parse_receipt_with_server(text):
    try:
        api_url = os.getenv("API_ENDPOINT", "http://localhost:5000")
        print(f"Sending request to: {api_url}/parse_receipt")
        print(f"Request payload: {{'text': {text}}}")
        response = requests.post(f"{api_url}/parse_receipt", json={'text': text})
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        response.raise_for_status()
        return response.json().get('response')
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Error response content: {e.response.text}")
        return None

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

    # Assume the server returns a string, parse it into a dictionary
    parsed_data = {}
    for line in receipt_data.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            parsed_data[key.strip()] = value.strip()

    confirmed_data = user_confirm_data(parsed_data)

    # Clean and convert the total amount
    total_str = confirmed_data.get('Total', '0')
    total_str = re.sub(r'[^\d.]', '', total_str)
    
    try:
        total_float = float(total_str)
    except ValueError:
        print(f"Error: Unable to convert '{total_str}' to a float. Please enter the total manually.")
        total_float = float(input("Enter the total amount as a number (e.g., 29.01): "))

    # Prepare data for API
    api_data = {
        'date': confirmed_data.get('Date', datetime.now().isoformat()),
        'category': confirmed_data.get('Category', 'Other'),
        'total': total_float
    }

    # Send data to API
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