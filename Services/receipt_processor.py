import io
import json
import os
import cv2
import pytesseract
from PIL import Image
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv


# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Windows
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract' # Mac OS
print("*******")
print(f"file path: {__name__}")
print(pytesseract.pytesseract.tesseract_cmd)
print("*******")

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def preprocess_image(receipts_object):
    try:
        # Convert file object to a numpy array
        image_bytes = np.frombuffer(receipts_object.read(), np.uint8)

        # Decode the image from the numpy array
        img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError(
                "Unable to decode the image. The file may be corrupted or in an unsupported format."
            )

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply thresholding
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        return thresh
    except Exception as e:
        print(f"Error in image preprocessing: {str(e)}")
        return None


def extract_text(preprocessed_image):
    try:

        text = pytesseract.image_to_string(Image.fromarray(preprocessed_image))
        # return json.dumps({"text": text})
        return text

    except Exception as e:
        print(f"Error in text extraction: {str(e)}")
        return None


def parse_receipt(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a receipt parser. Extract the date, total amount, and category.",
            },
            {"role": "user", "content": f"Parse this receipt to json: {text}"},
        ],
    )
    parsed_data = response.choices[0].message.content
    return parsed_data


def process_receipt(receipts_object):
    preprocessed = preprocess_image(receipts_object)
    if preprocessed is None:
        return None
    text = extract_text(preprocessed)
    if text is None:
        return None

    parsed = parse_receipt(text)
    if parsed is None:
        return None
    return parsed
    # return json.loads(parsed)

def convert_text_receipt_to_json_with_status_unverified(text):
    try:
        obj = json.loads(text)
        obj['status'] = 'unverified'
        return obj
    except Exception as e:
        print(f"Error in convert_text_receipt_to_json: {str(e)}")
        return None

def process_list_of_receipts(receipts_objects):
    try:
        text_images = []
        for receipts_object in receipts_objects:
            image_bytes = receipts_object.read()
            image_file = io.BytesIO(image_bytes)
            processed_image_text = process_receipt(image_file)
            if processed_image_text is None:
                return None
            text_images.append(processed_image_text)
            # processed_images_array_json = list(lambda x: json.loads(x), text_images)
            processed_images_array_json = [convert_text_receipt_to_json_with_status_unverified(x) for x in text_images]
            return processed_images_array_json
    except Exception as e:
        print(f"Error in receipt processing: {str(e)}")
        return None
