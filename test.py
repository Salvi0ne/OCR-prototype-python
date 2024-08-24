import cv2
import pytesseract
from PIL import Image
import re
import os
import openai
import json
import requests
from datetime import datetime

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

def parse_receipt_with_openai(text):
    try:
        prompt = f"""
        Analyze the following receipt text and extract the following information:
        1. Date of purchase (in any format)
        2. Total amount spent
        3. Category of spending (Food, Lodging, Transportation, or Other)

        Receipt text:
        {text}

        Respond in JSON format with keys: date, total, category
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes receipt text."},
                {"role": "user", "content": prompt}
            ]
        )

        # Print raw AI response for debugging
        print("Raw AI response:")
        print(response.choices[0].message.content)

        # Try to parse the JSON response
        try:
            ai_response = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract information using regex
            content = response.choices[0].message.content
            date_match = re.search(r'"date"\s*:\s*"([^"]+)"', content)
            total_match = re.search(r'"total"\s*:\s*"([^"]+)"', content)
            category_match = re.search(r'"category"\s*:\s*"([^"]+)"', content)

            ai_response = {
                'date': date_match.group(1) if date_match else "Date not found",
                'total': total_match.group(1) if total_match else "Total not found",
                'category': category_match.group(1) if category_match else "Category not found"
            }

        return {
            'Date': ai_response.get('date', "Date not found"),
            'Total': ai_response.get('total', "Total not found"),
            'Category': ai_response.get('category', "Category not found")
        }
    except Exception as e:
        print(f"Error in AI-based receipt parsing: {str(e)}")
        return None

def user_confirm_data(data):
    print("\nExtracted Data:")
    for key, value in data.items():
        print(f"{key}: {value}")
    
    while True:
        confirm = input("\nIs this information correct? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            return data
        elif confirm in ['no', 'n']:
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

    receipt_data = parse_receipt_with_openai(text)
    if receipt_data is None:
        return None

    confirmed_data = user_confirm_data(receipt_data)

    # Clean and convert the total amount
    total_str = confirmed_data['Total']
    total_str = re.sub(r'[^\d.]', '', total_str)  # Remove all non-digit and non-decimal point characters
    
    try:
        total_float = float(total_str)
    except ValueError:
        print(f"Error: Unable to convert '{confirmed_data['Total']}' to a float. Please enter the total manually.")
        total_float = float(input("Enter the total amount as a number (e.g., 29.01): "))

    # Prepare data for API
    api_data = {
        'date': confirmed_data['Date'],
        'category': confirmed_data['Category'],
        'total': total_float
    }

    # Send data to API
    api_url = "http://localhost:5000/receipts"
    try:
        response = requests.post(api_url, json=api_data)
        if response.status_code == 201:
            receipt_id = list(response.json().keys())[0]
            print(f"Receipt data sent successfully. Receipt ID: {receipt_id}")
        else:
            print(f"Failed to send receipt data: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending data to API: {str(e)}")

    return confirmed_data

# Main execution
if __name__ == "__main__":
    while True:
        image_path = input("Enter the path to the receipt image (or 'quit' to exit): ")
        if image_path.lower() == 'quit':
            break

        processed_data = process_receipt(image_path)
        if processed_data:
            print("\nProcessed and Sent Receipt Data:")
            for key, value in processed_data.items():
                print(f"{key}: {value}")
        else:
            print("Failed to process the receipt. Please try again with a different image.")