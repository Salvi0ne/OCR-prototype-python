# OCR Receipt Processor

## Design

- Go to design>OCR.excalidraw, export this file to https://excalidraw.com/ or click here [excalidraw](https://excalidraw.com/) to see the design..


## DEV

This Python script processes receipt images using OCR technology. It extracts date and total amount information, categorizes spending, and saves the data to an Excel file. Features include:

- Image preprocessing
- Text extraction using Tesseract OCR
- Date and total amount parsing
- Spending categorization
- User confirmation of extracted data
- Excel output

Requirements: OpenCV, Pytesseract, Pillow, pandas, openpyxl, postgresql
pip install flask flask_sqlalchemy psycopg2-binary python-dotenv - for app.py

Usage: Run `main()` function and follow prompts to input receipt image paths.

Note: This is a prototype with room for improvement in accuracy and feature set.

## LINK
https://github.com/Salvi0ne/OCR-prototype-python
