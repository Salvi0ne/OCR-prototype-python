import json
import pandas as pd

# Sample JSON data as a string
json_data = '''
{
  "employees": [
    {
      "id": 1,
      "name": "John Doe",
      "department": "HR",
      "salary": 50000
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "department": "Finance",
      "salary": 60000
    },
    {
      "id": 3,
      "name": "Michael Johnson",
      "department": "IT",
      "salary": 75000
    }
  ]
}
'''

# Convert JSON string to Python dict
data = json.loads(json_data)

# Convert dict to pandas DataFrame
df = pd.DataFrame(data['employees'])

# Save DataFrame to Excel file
file_path = 'employees.xlsx'
df.to_excel(file_path, index=False)

file_path
