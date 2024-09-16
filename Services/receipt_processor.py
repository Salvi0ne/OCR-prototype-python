import cv2
import pytesseract
from PIL import Image
import numpy as np

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Windows
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract' # Mac OS
print("*******")
print(f"file path: {__name__}")
print(pytesseract.pytesseract.tesseract_cmd)
print("*******")

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
        return pytesseract.image_to_string(Image.fromarray(preprocessed_image))
    except Exception as e:
        print(f"Error in text extraction: {str(e)}")
        return None


def process_receipt(receipts_object):
    preprocessed = preprocess_image(receipts_object)
    if preprocessed is None:
        return None

    text = extract_text(preprocessed)

    if text is None:
        return None
    # print(text)
    # print("---end----")
    return text
