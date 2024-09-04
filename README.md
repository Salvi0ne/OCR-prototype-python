# OCR Receipt Processor

-  Install Python 3.8 or higher if not already installed.

-  Clone the repository (if not already done):
   git clone [repository_url]
   cd [repository_name]

-  Create a virtual environment:
   python -m venv venv

-  Activate the virtual environment:
   - On Windows: venv\Scripts\activate
   - On macOS/Linux: source venv/bin/activate

-  Install required packages:
   pip install -r requirements.txt

-  Place the .env file in the project root directory (this file should be provided to you separately).

-  Download the Cloud SQL Proxy:
   - Go to: https://cloud.google.com/sql/docs/mysql/connect-admin-proxy#install
   - Download the appropriate version for your operating system
   - Rename the downloaded file to "cloud_sql_proxy" (add .exe extension on Windows if it's not already there)
   - Move the file to the project root directory

-  Run the Cloud SQL Proxy:
   - Open a command prompt/terminal in the project directory
   - Run: cloud_sql_proxy chrome-era-432100-q9:us-central1:receipts-data --port 5433
   - Keep this window open while working on the project

-  In a new command prompt/terminal, activate the virtual environment (step and run the Flask app:
   python app.py

-  To process a receipt, run in another command prompt/terminal (with venv activated):
    python test.py

-  To fetch data from the database, run:
    python fetchfromdb.py

Note: Always ensure the Cloud SQL Proxy is running when working with the application.

If you encounter any issues, please contact [Your Name/Contact Info].


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

## LINK
https://github.com/Salvi0ne/OCR-prototype-python

## File Naming Conventions
- https://google.github.io/styleguide/pyguide.html#3164-guidelines-derived-from-guidos-recommendations

## API (In Progress)

- API Server based on Rest API
- To run API Server, run on your terminal: 

```bash
python/python3 API/app.py
```







