# OCR Receipt Backend

This Python script serves as the backend API for processing receipts.

## Prerequisites

- Install Python 3.8 or higher if not already installed.
- Install required dependencies using pip/pip3:
    ```bash
    pip3 install -r requirements.txt
    ```

- Create a `.env` file with the following environment variables:

  1. `DATABASE_URL` (for Flask SQLAlchemy)
      **Example**:
      ```plaintext
      DATABASE_URL=postgresql://postgres_local:abc123@localhost/hello_world
      ```

  2. `OPENAI_API_KEY` (for accessing OpenAI API)


### Running the Server

The script hardcode localhost port ***5001*** 

To change the port - go to `app.py` and change port=` 5001`

```
app.run(host="0.0.0.0", port=5001, debug=True)
```


To start the server, run the following command in your terminal:

- Use either `python` or `python3`:

```bash
python app.py
```

### PostgreSQL Database Connection

To configure the PostgreSQL database connection, follow these steps:

1. Add the following configuration to your `.env` file:

    ```plaintext
    DATABASE_URL=postgresql://<username>:<password>@<host>/<database_name>
    ```

2. Replace the placeholders with the appropriate values:
    - **`<username>`**: Your PostgreSQL username (e.g., `postgres_local`)
    - **`<password>`**: The password for the PostgreSQL user (leave blank if not required)
    - **`<host>`**: The database host (e.g., `localhost` for local development)
    - **`<database_name>`**: The name of your PostgreSQL database (e.g., `hello_world`)

### To Run All Tests:
 Use either `python` or `python3`:
    ```bash
    python -m pytest -s
    ```
    ***Or***
    ```bash
    python3 -m pytest -s
    ```

***Note:*** There are currently only a few tests available, but more will be added over time.

### Every file suggestion:

File Naming convenstions based on https://google.github.io/styleguide/pyguide.html#3164-guidelines-derived-from-guidos-recommendations
- prefix file name ( eg: test_*.py )
- file name use `snake_case` ( eg: test_snake_case )
- test class use `PascalCase` ( eg: class TestPascalCase(unittest.TestCase) ) 

## LINK
https://github.com/Salvi0ne/OCR-prototype-python

### OPTIONAL

-  Create a virtual environment:
   python -m venv venv

-  Activate the virtual environment:
   - On Windows: venv\Scripts\activate
   - On macOS/Linux: source venv/bin/activate


-  Download the Cloud SQL Proxy:
   - Go to: https://cloud.google.com/sql/docs/mysql/connect-admin-proxy#install
   - Download the appropriate version for your operating system
   - Rename the downloaded file to "cloud_sql_proxy" (add .exe extension on Windows if it's not already there)
   - Move the file to the project root directory

-  Run the Cloud SQL Proxy:
   - Open a command prompt/terminal in the project directory
   - Run: cloud_sql_proxy chrome-era-432100-q9:us-central1:receipts-data --port 5433
   - Keep this window open while working on the project 


### API DOCUMENTATION : 


***Response Structure***

- Eg Error Structure:
```json
{ 
    "code": 400,
    "data": null,
    "message": "",
    "messages": [],
    "status_code": "Bad Request"
}
```

- Eg Success Structure:
```json
{
    "code": 200,
    "data": null,
    "message": "OK",
    "messages": [],
    "status_code": ["OK"]
}
```
---

To test the API endpoints, you can use a tool like curl or a REST client like Postman.
For example, to initialize the system, you can use the following command:
`curl -X GET http://127.0.0.1:5001/api/initx`


---


***Backend/Routes/routes.py:***

#### 1. Get All Receipts by Status
**Endpoint:** `GET /api/receipts/<string:status>`

**Example Endpoint:** http://127.0.0.1:5001/api/receipts/verified

 **Parameters:**
  - `status`: Must be either `verified` or `unverified`.

**Response:**
  - Returns all receipts with the specified status.

**Example Response:**
```json
{
    "code": 200,
    "data": [
        {
            "id": "c433ca2d-0f06-4d43-acb9-3698f2e828a2",
            "total_amount": 10.10,
            "category": "dining",
            "status": "unverified",
            "date": "10/10/2024",
            "date_created": "2024-09-23T10:15:30",
            "date_updated": null,
        },

    ],
    "message": "Retrieved Receipts status: unverified",
    "messages": [],
    "status_code": ["OK"]
}
```

---
#### 2. Extract Receipts from Image
**Endpoint:** `POST /api/extract_receipts`

**Example Endpoint:** http://127.0.0.1:5001/api/extract_receipts

**Body:**
  - `files`: List of image files to process.

**Response:**
  - """Extract receipts from image"""

## ##DEV## UPDATE TIME TO TIME 
